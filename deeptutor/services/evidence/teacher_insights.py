from __future__ import annotations

from collections import defaultdict
from typing import Any


_CONFIDENCE_SCORE = {"high": 3, "medium": 2, "low": 1}


def _top_inferred(payload: dict[str, Any]) -> dict[str, Any] | None:
    inferred = payload.get("inferred") or []
    if not inferred:
        return None
    return inferred[0]


def _top_action(payload: dict[str, Any]) -> dict[str, Any] | None:
    actions = payload.get("recommended_actions") or []
    if not actions:
        return None
    return actions[0]


def build_teacher_insights_payload(
    *,
    student_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    grouped: dict[tuple[str, str, str], list[tuple[str, int]]] = defaultdict(list)
    for payload in student_payloads:
        inferred = _top_inferred(payload)
        action = _top_action(payload)
        if not inferred or not action:
            continue
        key = (
            str(inferred.get("topic") or "general"),
            str(inferred.get("diagnosis_type") or "low_confidence"),
            str(action.get("action_type") or "small_group_support"),
        )
        grouped[key].append(
            (
                str(payload.get("student_id") or "unknown"),
                _CONFIDENCE_SCORE.get(str(inferred.get("confidence_tag") or "low"), 1),
            )
        )

    small_groups: list[dict[str, Any]] = []
    for (topic, diagnosis_type, action_type), rows in grouped.items():
        if len(rows) < 2:
            continue
        confidence_sum = sum(score for _sid, score in rows)
        avg_confidence = confidence_sum / float(len(rows))
        if avg_confidence < 1.0:
            continue
        student_ids = sorted({sid for sid, _score in rows})
        small_groups.append(
            {
                "topic": topic,
                "diagnosis_type": diagnosis_type,
                "student_ids": student_ids,
                "recommended_action": "small_group_support",
                "source_action_type": action_type,
                "confidence_tag": "high" if avg_confidence >= 2.5 else "medium",
            }
        )

    small_groups.sort(
        key=lambda row: (-len(row["student_ids"]), row["topic"], row["diagnosis_type"], row["source_action_type"])
    )

    return {
        "students": student_payloads,
        "small_groups": small_groups,
    }
