"""
Unified session history API.
"""

from __future__ import annotations

from typing import Any
from enum import Enum

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query

from deeptutor.services.session import (
    extract_assessment_review,
    get_assessment_rubric_review,
    get_sqlite_session_store,
    upsert_assessment_rubric_review,
)

router = APIRouter()


class SessionRenameRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class QuizResultItem(BaseModel):
    question_id: str = ""
    question: str = Field(..., min_length=1)
    user_answer: str = ""
    correct_answer: str = ""
    is_correct: bool
    duration_seconds: int | None = Field(default=None, ge=0)


class QuizResultsRequest(BaseModel):
    answers: list[QuizResultItem] = Field(default_factory=list)


class AssessmentRubricLevel(str, Enum):
    strong = "strong"
    acceptable = "acceptable"
    weak = "weak"


class AssessmentRubricDecision(str, Enum):
    approved_for_reuse = "approved_for_reuse"
    needs_edit_before_reuse = "needs_edit_before_reuse"
    not_ready = "not_ready"


class TeacherAssessmentReviewRequest(BaseModel):
    wording_quality: AssessmentRubricLevel
    distractor_quality: AssessmentRubricLevel
    explanation_clarity: AssessmentRubricLevel
    overall_decision: AssessmentRubricDecision
    teacher_note: str = ""


def _clip_text(value: str, limit: int = 280) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _session_knowledge_bases(session: dict[str, Any]) -> list[str]:
    preferences = session.get("preferences")
    if not isinstance(preferences, dict):
        return []
    raw = preferences.get("knowledge_bases", [])
    if not isinstance(raw, list):
        return []
    return [str(item).strip() for item in raw if str(item).strip()]


def _latest_message_content(session: dict[str, Any], role: str) -> str | None:
    for message in reversed(session.get("messages", [])):
        if str(message.get("role") or "") != role:
            continue
        content = _clip_text(str(message.get("content") or ""))
        if content:
            return content
    return None


def _normalize_followup_questions(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    questions: list[str] = []
    for item in raw:
        question = str(item or "").strip()
        if question:
            questions.append(question)
        if len(questions) == 3:
            break
    return questions


def _extract_followup_questions(session: dict[str, Any]) -> list[str]:
    for message in reversed(session.get("messages", [])):
        events = message.get("events")
        if not isinstance(events, list):
            continue
        for event in reversed(events):
            if not isinstance(event, dict) or str(event.get("type") or "") != "result":
                continue
            metadata = event.get("metadata")
            if not isinstance(metadata, dict):
                continue
            session_context = metadata.get("session_context")
            if isinstance(session_context, dict):
                questions = _normalize_followup_questions(session_context.get("followup_questions"))
                if questions:
                    return questions
            questions = _normalize_followup_questions(metadata.get("followup_questions"))
            if questions:
                return questions
    return []


def _build_context_support(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "knowledge_bases": _session_knowledge_bases(session),
        "conversation_summary": _clip_text(str(session.get("compressed_summary") or ""), limit=400),
        "last_user_message": _latest_message_content(session, "user"),
        "last_assistant_message": _latest_message_content(session, "assistant"),
        "followup_questions": _extract_followup_questions(session),
    }


def _build_review_context_support(
    session: dict[str, Any],
    review: dict[str, Any],
) -> dict[str, Any]:
    incorrect_results = [
        {
            "question_id": item.get("question_id"),
            "question": item.get("question"),
            "correct_answer": item.get("correct_answer"),
        }
        for item in review.get("results", [])
        if not item.get("is_correct")
    ][:3]
    support = _build_context_support(session)
    support["incorrect_questions"] = incorrect_results
    return support


def _format_quiz_results_message(answers: list[QuizResultItem]) -> str:
    total = len(answers)
    correct = sum(1 for item in answers if item.is_correct)
    score_pct = round((correct / total) * 100) if total else 0
    lines = ["[Quiz Performance]"]
    for idx, item in enumerate(answers, 1):
        question = item.question.strip().replace("\n", " ")
        user_answer = (item.user_answer or "").strip() or "(blank)"
        status = "Correct" if item.is_correct else "Incorrect"
        details = [status]
        if not item.is_correct and (item.correct_answer or "").strip():
            details.append(f"correct: {(item.correct_answer or '').strip()}")
        if item.duration_seconds is not None:
            details.append(f"time: {item.duration_seconds}s")
        qid = f"[{item.question_id}] " if item.question_id else ""
        lines.append(f"{idx}. {qid}Q: {question} -> Answered: {user_answer} ({', '.join(details)})")
    lines.append(f"Score: {correct}/{total} ({score_pct}%)")
    return "\n".join(lines)


@router.get("")
async def list_sessions(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=offset)
    return {"sessions": sessions}


@router.get("/{session_id}")
async def get_session(session_id: str):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        **session,
        "context_support": _build_context_support(session),
    }


@router.get("/{session_id}/assessment-review")
async def get_assessment_review(session_id: str):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    review = extract_assessment_review(session)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")
    review["teacher_review"] = get_assessment_rubric_review(store.db_path, session_id)
    return {
        **review,
        "context_support": _build_review_context_support(session, review),
    }


@router.post("/{session_id}/assessment-rubric-review")
async def create_assessment_rubric_review(session_id: str, payload: TeacherAssessmentReviewRequest):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    review = extract_assessment_review(session)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")
    return upsert_assessment_rubric_review(store.db_path, session_id, payload.model_dump())


@router.patch("/{session_id}/assessment-rubric-review")
async def update_assessment_rubric_review(session_id: str, payload: TeacherAssessmentReviewRequest):
    store = get_sqlite_session_store()
    session = await store.get_session_with_messages(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    review = extract_assessment_review(session)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")
    return upsert_assessment_rubric_review(store.db_path, session_id, payload.model_dump())


@router.patch("/{session_id}")
async def rename_session(session_id: str, payload: SessionRenameRequest):
    store = get_sqlite_session_store()
    updated = await store.update_session_title(session_id, payload.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Session not found")
    session = await store.get_session(session_id)
    return {"session": session}


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    store = get_sqlite_session_store()
    deleted = await store.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"deleted": True, "session_id": session_id}


@router.post("/{session_id}/quiz-results")
async def record_quiz_results(session_id: str, payload: QuizResultsRequest):
    if not payload.answers:
        raise HTTPException(status_code=400, detail="Quiz results are required")
    store = get_sqlite_session_store()
    session = await store.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    content = _format_quiz_results_message(payload.answers)
    await store.add_message(
        session_id=session_id,
        role="user",
        content=content,
        capability="deep_question",
    )
    return {
        "recorded": True,
        "session_id": session_id,
        "answer_count": len(payload.answers),
        "content": content,
    }
