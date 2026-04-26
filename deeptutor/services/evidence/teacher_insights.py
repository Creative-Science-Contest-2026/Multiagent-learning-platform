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


def _student_actions(student_id: str, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        action
        for action in actions
        if action.get("target_type") == "student" and action.get("target_id") == student_id
    ]
    return sorted(rows, key=lambda row: row.get("updated_at", 0), reverse=True)


def _student_assignments(student_id: str, assignments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        assignment
        for assignment in assignments
        if assignment.get("target_type") == "student" and assignment.get("target_id") == student_id
    ]
    return sorted(rows, key=lambda row: row.get("updated_at", 0), reverse=True)


def _small_group_target_id(topic: str, diagnosis_type: str, source_action_type: str) -> str:
    return f"{topic}::{diagnosis_type}::{source_action_type}"


def build_teacher_insights_payload(
    *,
    student_payloads: list[dict[str, Any]],
    teacher_actions: list[dict[str, Any]] | None = None,
    intervention_assignments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    teacher_actions = teacher_actions or []
    intervention_assignments = intervention_assignments or []
    grouped: dict[tuple[str, str, str], list[tuple[str, int]]] = defaultdict(list)
    students: list[dict[str, Any]] = []
    for payload in student_payloads:
        row = dict(payload)
        row["teacher_actions"] = _student_actions(str(payload.get("student_id") or "unknown"), teacher_actions)
        row["intervention_assignments"] = _student_assignments(
            str(payload.get("student_id") or "unknown"),
            intervention_assignments,
        )
        students.append(row)
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
        target_id = _small_group_target_id(topic, diagnosis_type, action_type)
        matching_group_action = next(
            (
                action
                for action in teacher_actions
                if action.get("target_type") == "small_group" and action.get("target_id") == target_id
            ),
            None,
        )
        matching_group_assignment = next(
            (
                assignment
                for assignment in intervention_assignments
                if assignment.get("target_type") == "small_group" and assignment.get("target_id") == target_id
            ),
            None,
        )
        small_groups.append(
            {
                "topic": topic,
                "diagnosis_type": diagnosis_type,
                "student_ids": student_ids,
                "recommended_action": "small_group_support",
                "source_action_type": action_type,
                "confidence_tag": "high" if avg_confidence >= 2.5 else "medium",
                "target_id": target_id,
                "teacher_action": matching_group_action,
                "intervention_assignment": matching_group_assignment,
            }
        )

    small_groups.sort(
        key=lambda row: (-len(row["student_ids"]), row["topic"], row["diagnosis_type"], row["source_action_type"])
    )

    return {
        "students": students,
        "small_groups": small_groups,
    }
