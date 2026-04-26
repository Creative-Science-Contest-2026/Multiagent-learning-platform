from __future__ import annotations

import math
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


def _compute_latency_seconds(turn_events: list[dict[str, Any]] | None) -> int | None:
    if not turn_events:
        return None
    timestamps = [float(event.get("timestamp") or 0) for event in turn_events if event.get("timestamp")]
    if len(timestamps) < 2:
        return None
    duration = int(max(timestamps) - min(timestamps))
    return max(0, duration)


def _infer_hint_count(assistant_message: str, followup_context: dict[str, Any] | None) -> int:
    followup_hint = 1 if isinstance(followup_context, dict) and followup_context.get("is_correct") is False else 0
    text = assistant_message.lower()
    lexical_hint = text.count("hint") + text.count("try this") + text.count("let's break")
    return max(followup_hint, min(3, lexical_hint))


def _infer_retry_count(user_message: str, followup_context: dict[str, Any] | None) -> int:
    if isinstance(followup_context, dict) and followup_context.get("is_correct") is False:
        return 1
    lowered = user_message.lower()
    retry_markers = ["again", "retry", "still", "i don't understand", "wrong"]
    return 1 if any(marker in lowered for marker in retry_markers) else 0


def extract_observations_from_tutoring_turn(
    *,
    session_id: str,
    student_id: str,
    user_message: str,
    assistant_message: str,
    followup_question_context: dict[str, Any] | None = None,
    turn_events: list[dict[str, Any]] | None = None,
) -> list[ObservationRecord]:
    context = followup_question_context if isinstance(followup_question_context, dict) else {}
    reference_question = str(context.get("question") or "").strip()
    topic_seed = reference_question or user_message
    topic = infer_topic_from_question(topic_seed, fallback="general")

    is_correct_raw = context.get("is_correct")
    is_correct = bool(is_correct_raw) if isinstance(is_correct_raw, bool) else True
    retry_count = _infer_retry_count(user_message, context)
    hint_count = _infer_hint_count(assistant_message, context)
    latency_seconds = _compute_latency_seconds(turn_events)

    dominant_error: str | None = None
    if not is_correct:
        dominant_error = "careless_error" if (latency_seconds or 0) <= 15 else "needs_scaffold"

    return [
        {
            "observation_id": f"obs_{uuid.uuid4().hex[:12]}",
            "session_id": session_id,
            "student_id": student_id or session_id or "unknown",
            "source": "tutoring",
            "topic": topic,
            "question_id": str(context.get("question_id") or ""),
            "is_correct": is_correct,
            "latency_seconds": latency_seconds,
            "hint_count": hint_count,
            "retry_count": retry_count,
            "dominant_error": dominant_error,
        }
    ]


def recency_weight(age_seconds: float) -> float:
    # Half-life weighting keeps recent mistakes dominant while preserving long-tail signal.
    half_life_seconds = 7 * 24 * 60 * 60
    if age_seconds <= 0:
        return 1.0
    return math.exp(-float(age_seconds) * math.log(2) / half_life_seconds)


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
