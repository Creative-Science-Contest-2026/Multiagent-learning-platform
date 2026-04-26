from __future__ import annotations

from collections import defaultdict
from typing import Any


def build_teacher_insights_payload(
    *,
    student_payloads: list[dict[str, Any]],
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for payload in student_payloads:
        inferred = payload.get("inferred") or []
        if not inferred:
            continue
        key = (inferred[0]["topic"], inferred[0]["diagnosis_type"])
        grouped[key].append(payload["student_id"])

    small_groups = [
        {
            "topic": topic,
            "diagnosis_type": diagnosis_type,
            "student_ids": sorted(student_ids),
            "recommended_action": "small_group_support",
        }
        for (topic, diagnosis_type), student_ids in grouped.items()
        if len(student_ids) >= 2
    ]

    return {
        "students": student_payloads,
        "small_groups": small_groups,
    }
