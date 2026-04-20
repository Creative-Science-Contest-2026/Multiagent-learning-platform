from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from deeptutor.services.assessment import recommend_next_assessment
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
