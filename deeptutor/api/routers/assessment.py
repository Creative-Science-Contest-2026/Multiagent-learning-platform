from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from deeptutor.services.assessment import recommend_next_assessment
from deeptutor.services.evidence.diagnosis import build_student_diagnosis
from deeptutor.services.evidence.extractor import extract_observations_from_review
from deeptutor.services.session import extract_assessment_review, get_sqlite_session_store

router = APIRouter()


class AssessmentRecommendationRequest(BaseModel):
    session_id: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


async def _collect_assessment_rows(
    *,
    session_id: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0)
    rows: list[dict[str, Any]] = []

    for session in sessions:
        capability = str(session.get("capability") or "chat")
        if capability != "deep_question":
            continue
        detail = await store.get_session_with_messages(str(session.get("session_id") or session.get("id")))
        if detail is None:
            continue
        review = extract_assessment_review(detail)
        if review is None:
            continue
        rows.append(
            {
                "session_id": review["session_id"],
                "timestamp": review["timestamp"],
                "summary": review["summary"],
                "knowledge_bases": review["knowledge_bases"],
                "assessment_results": review["results"],
            }
        )

    if session_id is not None:
        rows.sort(key=lambda row: row["session_id"] != session_id)

    return rows


@router.post("/recommend")
async def recommend_assessment(payload: AssessmentRecommendationRequest):
    rows = await _collect_assessment_rows(session_id=payload.session_id, limit=payload.limit)
    return recommend_next_assessment(rows, preferred_session_id=payload.session_id)


@router.get("/diagnosis/{session_id}")
async def get_assessment_diagnosis(session_id: str):
    store = get_sqlite_session_store()
    detail = await store.get_session_with_messages(session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Assessment session not found")

    review = extract_assessment_review(detail)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")

    review["student_id"] = str((detail.get("preferences") or {}).get("student_id") or session_id)
    observations = extract_observations_from_review(review)
    await store.save_observations(observations)

    student_id = review["student_id"]
    state = {
        "student_id": student_id,
        "repeated_mistakes": sorted({row["topic"] for row in observations if not row["is_correct"]}),
        "support_level": "guided" if any(not row["is_correct"] for row in observations) else "independent",
        "confidence_trend": "down" if any(not row["is_correct"] for row in observations) else "flat",
    }
    await store.upsert_student_state(student_id, state)

    return build_student_diagnosis(
        student_id=student_id,
        observations=observations,
        student_state=await store.get_student_state(student_id),
    )
