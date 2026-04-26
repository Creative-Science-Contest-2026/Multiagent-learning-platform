from __future__ import annotations

from collections import Counter
from typing import Any


def _confidence_tag(observations: list[dict[str, Any]]) -> str:
    if len(observations) >= 3:
        return "high"
    if len(observations) == 2:
        return "medium"
    return "low"


def _support_level(observations: list[dict[str, Any]]) -> str:
    if any((row.get("hint_count") or 0) >= 2 for row in observations):
        return "intensive"
    if any(not row.get("is_correct") for row in observations):
        return "guided"
    return "independent"


def build_student_diagnosis(
    *,
    student_id: str,
    observations: list[dict[str, Any]],
    student_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not observations:
        return {
            "student_id": student_id,
            "observed": None,
            "student_state": student_state,
            "inferred": [],
            "recommended_actions": [],
        }

    topic_counter = Counter(row["topic"] for row in observations if not row.get("is_correct"))
    if topic_counter:
        dominant_topic, _ = topic_counter.most_common(1)[0]
        dominant_rows = [row for row in observations if row["topic"] == dominant_topic]
    else:
        dominant_rows = observations
        dominant_topic = observations[0]["topic"]

    error_counter = Counter(row["dominant_error"] for row in dominant_rows if row.get("dominant_error"))
    dominant_error = error_counter.most_common(1)[0][0] if error_counter else "low_confidence"
    confidence = _confidence_tag(dominant_rows)
    avg_latency_values = [
        int(row.get("latency_seconds") or 0)
        for row in dominant_rows
        if row.get("latency_seconds") is not None
    ]
    derived_state = student_state or {
        "student_id": student_id,
        "repeated_mistakes": [dominant_topic],
        "support_level": _support_level(dominant_rows),
        "confidence_trend": "down",
    }
    recommendation_type = "review_prerequisite" if dominant_error == "concept_gap" else "increase_scaffold"

    return {
        "student_id": student_id,
        "observed": {
            "topic": dominant_topic,
            "miss_count": sum(1 for row in dominant_rows if not row.get("is_correct")),
            "avg_latency_seconds": round(sum(avg_latency_values) / len(avg_latency_values))
            if avg_latency_values
            else 0,
        },
        "student_state": derived_state,
        "inferred": [
            {
                "diagnosis_type": dominant_error,
                "confidence_tag": confidence,
                "topic": dominant_topic,
                "evidence": [
                    f"{len(dominant_rows)} missed question(s) in {dominant_topic}",
                    f"support_level={_support_level(dominant_rows)}",
                ],
            }
        ],
        "recommended_actions": [
            {
                "action_id": f"{student_id}:{dominant_topic}:{recommendation_type}",
                "action_type": recommendation_type,
                "target_student_ids": [student_id],
                "topic": dominant_topic,
                "rationale": f"Revisit {dominant_topic} before moving to mixed practice.",
            }
        ],
    }
