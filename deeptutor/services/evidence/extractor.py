from __future__ import annotations

import uuid
from typing import Any

from deeptutor.services.assessment.analysis import infer_topic_from_question

from .contracts import ObservationRecord


def _dominant_error(result: dict[str, Any], repeated_topic_misses: int) -> str | None:
    if bool(result.get("is_correct")):
        return None
    duration = int(result.get("duration_seconds") or 0)
    if repeated_topic_misses >= 2:
        return "concept_gap"
    if duration <= 15:
        return "careless_error"
    return "needs_scaffold"


def extract_observations_from_review(review: dict[str, Any]) -> list[ObservationRecord]:
    results = review.get("results") if isinstance(review.get("results"), list) else []
    topic_miss_counts: dict[str, int] = {}
    for item in results:
        topic = infer_topic_from_question(str(item.get("question") or ""), fallback="general")
        if not bool(item.get("is_correct")):
            topic_miss_counts[topic] = topic_miss_counts.get(topic, 0) + 1

    rows: list[ObservationRecord] = []
    for item in results:
        topic = infer_topic_from_question(str(item.get("question") or ""), fallback="general")
        rows.append(
            {
                "observation_id": f"obs_{uuid.uuid4().hex[:12]}",
                "session_id": str(review.get("session_id") or ""),
                "student_id": str(review.get("student_id") or review.get("session_id") or "unknown"),
                "source": "assessment",
                "topic": topic,
                "question_id": str(item.get("question_id") or ""),
                "is_correct": bool(item.get("is_correct")),
                "latency_seconds": int(item.get("duration_seconds")) if item.get("duration_seconds") else None,
                "hint_count": int(item.get("hint_count") or 0),
                "retry_count": int(item.get("retry_count") or 0),
                "dominant_error": _dominant_error(item, topic_miss_counts.get(topic, 0)),
            }
        )
    return rows
