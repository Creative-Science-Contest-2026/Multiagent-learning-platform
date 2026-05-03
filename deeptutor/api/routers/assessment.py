from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from deeptutor.services.auth.deps import owner_scope_for_user
from deeptutor.services.auth.deps import require_roles
from deeptutor.services.auth.schemas import AuthenticatedUser
from deeptutor.services.assessment import recommend_next_assessment
from deeptutor.services.evidence.diagnosis import build_student_diagnosis
from deeptutor.services.evidence.extractor import extract_observations_from_review
from deeptutor.services.session import extract_assessment_review, get_sqlite_session_store

router = APIRouter()
require_teacher_or_admin = require_roles("teacher", "admin")


class AssessmentRecommendationRequest(BaseModel):
    session_id: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


async def _collect_assessment_rows(
    *,
    session_id: str | None,
    limit: int,
    owner_user_id: str | None,
) -> list[dict[str, Any]]:
    store = get_sqlite_session_store()
    sessions = await store.list_sessions(limit=limit, offset=0, owner_user_id=owner_user_id)
    rows: list[dict[str, Any]] = []

    for session in sessions:
        capability = str(session.get("capability") or "chat")
        if capability != "deep_question":
            continue
        detail = await store.get_session_with_messages(
            str(session.get("session_id") or session.get("id")),
            owner_user_id=owner_user_id,
        )
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
async def recommend_assessment(
    payload: AssessmentRecommendationRequest,
    current_user: AuthenticatedUser = Depends(require_teacher_or_admin),
):
    rows = await _collect_assessment_rows(
        session_id=payload.session_id,
        limit=payload.limit,
        owner_user_id=owner_scope_for_user(current_user),
    )
    return recommend_next_assessment(rows, preferred_session_id=payload.session_id)


@router.get("/diagnosis/{session_id}")
async def get_assessment_diagnosis(
    session_id: str,
    current_user: AuthenticatedUser = Depends(require_teacher_or_admin),
):
    store = get_sqlite_session_store()
    owner_scope = owner_scope_for_user(current_user)
    detail = await store.get_session_with_messages(session_id, owner_user_id=owner_scope)
    if detail is None:
        raise HTTPException(status_code=404, detail="Assessment session not found")

    review = extract_assessment_review(detail)
    if review is None:
        raise HTTPException(status_code=404, detail="Assessment review not found")

    review["student_id"] = str((detail.get("preferences") or {}).get("student_id") or session_id)
    observations = extract_observations_from_review(review)
    await store.save_observations(observations, owner_user_id=owner_scope)

    student_id = review["student_id"]
    rollup = await store.build_student_state_rollup(student_id, owner_user_id=owner_scope)
    if rollup is not None:
        await store.upsert_student_state(student_id, rollup, owner_user_id=owner_scope)

    return build_student_diagnosis(
        student_id=student_id,
        observations=observations,
        student_state=await store.get_student_state(student_id, owner_user_id=owner_scope),
    )
