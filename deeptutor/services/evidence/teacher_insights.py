from __future__ import annotations

from collections import defaultdict
from typing import Any


_CONFIDENCE_SCORE = {"high": 3, "medium": 2, "low": 1}


def _top_inferred(payload: dict[str, Any]) -> dict[str, Any] | None:
    inferred = payload.get("inferred") or []
    if not inferred:
        return None
    return inferred[0]


def _latest_diagnosis_feedback(
    *,
    student_id: str,
    source_topic: str,
    source_diagnosis_type: str,
    diagnosis_feedback: list[dict[str, Any]],
) -> dict[str, Any] | None:
    return next(
        (
            row
            for row in diagnosis_feedback
            if row.get("student_id") == student_id
            and row.get("source_topic") == source_topic
            and row.get("source_diagnosis_type") == source_diagnosis_type
        ),
        None,
    )


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


def _student_intervention_history(
    *,
    student_id: str,
    recommendation_ack: dict[str, Any] | None,
    teacher_actions: list[dict[str, Any]],
    intervention_assignments: list[dict[str, Any]],
    diagnosis_feedback: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sequence = 0

    def add_row(row: dict[str, Any]) -> None:
        nonlocal sequence
        sequence += 1
        row["_sequence"] = sequence
        rows.append(row)

    if recommendation_ack:
        add_row(
            {
                "id": f"recommendation_ack:{recommendation_ack.get('id')}",
                "item_type": "recommendation_ack",
                "timestamp": int(recommendation_ack.get("updated_at") or recommendation_ack.get("created_at") or 0),
                "title": "Recommendation acknowledgement",
                "detail": str(recommendation_ack.get("teacher_note") or "Teacher acknowledged the recommendation."),
                "status": str(recommendation_ack.get("status") or "unknown"),
                "topic": "",
                "source_id": str(recommendation_ack.get("id") or ""),
            }
        )

    for action in teacher_actions:
        add_row(
            {
                "id": f"teacher_action:{action.get('id')}",
                "item_type": "teacher_action",
                "timestamp": int(action.get("updated_at") or action.get("created_at") or 0),
                "title": str(action.get("action_type") or "Teacher action"),
                "detail": str(action.get("teacher_instruction") or "No teacher instruction recorded."),
                "status": str(action.get("status") or "unknown"),
                "topic": str(action.get("topic") or ""),
                "source_id": str(action.get("id") or ""),
            }
        )

    for assignment in intervention_assignments:
        add_row(
            {
                "id": f"intervention_assignment:{assignment.get('id')}",
                "item_type": "intervention_assignment",
                "timestamp": int(assignment.get("updated_at") or assignment.get("created_at") or 0),
                "title": str(assignment.get("title") or assignment.get("assignment_type") or "Intervention assignment"),
                "detail": str(
                    assignment.get("teacher_note")
                    or assignment.get("practice_note")
                    or "No assignment detail recorded."
                ),
                "status": str(assignment.get("status") or "unknown"),
                "topic": "",
                "source_id": str(assignment.get("id") or ""),
            }
        )

    if diagnosis_feedback:
        add_row(
            {
                "id": f"diagnosis_feedback:{diagnosis_feedback.get('id')}",
                "item_type": "diagnosis_feedback",
                "timestamp": int(diagnosis_feedback.get("updated_at") or diagnosis_feedback.get("created_at") or 0),
                "title": "Diagnosis feedback",
                "detail": str(
                    diagnosis_feedback.get("teacher_note")
                    or "Teacher reviewed the diagnosis quality without leaving a note."
                ),
                "status": str(diagnosis_feedback.get("feedback_label") or "unknown"),
                "topic": str(diagnosis_feedback.get("source_topic") or ""),
                "source_id": str(diagnosis_feedback.get("id") or ""),
            }
        )

    ordered = sorted(rows, key=lambda row: (row.get("timestamp", 0), row.get("_sequence", 0)), reverse=True)
    for row in ordered:
        row.pop("_sequence", None)
    return ordered


def _latest_recommendation_ack(
    *,
    target_type: str,
    target_id: str,
    source_recommendation_id: str,
    recommendation_acks: list[dict[str, Any]],
) -> dict[str, Any] | None:
    return next(
        (
            row
            for row in recommendation_acks
            if row.get("target_type") == target_type
            and row.get("target_id") == target_id
            and row.get("source_recommendation_id") == source_recommendation_id
        ),
        None,
    )


def _latest_recommendation_feedback(
    *,
    target_type: str,
    target_id: str,
    source_recommendation_id: str,
    recommendation_feedback: list[dict[str, Any]],
) -> dict[str, Any] | None:
    return next(
        (
            row
            for row in recommendation_feedback
            if row.get("target_type") == target_type
            and row.get("target_id") == target_id
            and row.get("source_recommendation_id") == source_recommendation_id
        ),
        None,
    )


def _small_group_target_id(topic: str, diagnosis_type: str, source_action_type: str) -> str:
    return f"{topic}::{diagnosis_type}::{source_action_type}"


def build_teacher_insights_payload(
    *,
    student_payloads: list[dict[str, Any]],
    teacher_actions: list[dict[str, Any]] | None = None,
    intervention_assignments: list[dict[str, Any]] | None = None,
    recommendation_acks: list[dict[str, Any]] | None = None,
    recommendation_feedback: list[dict[str, Any]] | None = None,
    diagnosis_feedback: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    teacher_actions = teacher_actions or []
    intervention_assignments = intervention_assignments or []
    recommendation_acks = recommendation_acks or []
    recommendation_feedback = recommendation_feedback or []
    diagnosis_feedback = diagnosis_feedback or []
    grouped: dict[tuple[str, str, str], list[tuple[str, int]]] = defaultdict(list)
    students: list[dict[str, Any]] = []
    for payload in student_payloads:
        row = dict(payload)
        top_action = _top_action(payload)
        student_id = str(payload.get("student_id") or "unknown")
        top_inferred = _top_inferred(payload)
        row["diagnosis_feedback"] = (
            _latest_diagnosis_feedback(
                student_id=student_id,
                source_topic=str(top_inferred.get("topic") or "general"),
                source_diagnosis_type=str(top_inferred.get("diagnosis_type") or "low_confidence"),
                diagnosis_feedback=diagnosis_feedback,
            )
            if top_inferred
            else None
        )
        row["recommendation_ack"] = (
            _latest_recommendation_ack(
                target_type="student",
                target_id=student_id,
                source_recommendation_id=str(top_action.get("action_id") or f"student:{student_id}"),
                recommendation_acks=recommendation_acks,
            )
            if top_action
            else None
        )
        row["recommendation_feedback"] = (
            _latest_recommendation_feedback(
                target_type="student",
                target_id=student_id,
                source_recommendation_id=str(top_action.get("action_id") or f"student:{student_id}"),
                recommendation_feedback=recommendation_feedback,
            )
            if top_action
            else None
        )
        row["teacher_actions"] = _student_actions(student_id, teacher_actions)
        row["intervention_assignments"] = _student_assignments(
            student_id,
            intervention_assignments,
        )
        row["intervention_history"] = _student_intervention_history(
            student_id=student_id,
            recommendation_ack=row["recommendation_ack"],
            teacher_actions=row["teacher_actions"],
            intervention_assignments=row["intervention_assignments"],
            diagnosis_feedback=row["diagnosis_feedback"],
        )
        students.append(row)
        inferred = top_inferred
        action = top_action
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
        matching_group_ack = _latest_recommendation_ack(
            target_type="small_group",
            target_id=target_id,
            source_recommendation_id=f"group:{topic}:{diagnosis_type}",
            recommendation_acks=recommendation_acks,
        )
        matching_group_feedback = _latest_recommendation_feedback(
            target_type="small_group",
            target_id=target_id,
            source_recommendation_id=f"group:{topic}:{diagnosis_type}",
            recommendation_feedback=recommendation_feedback,
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
                "recommendation_ack": matching_group_ack,
                "recommendation_feedback": matching_group_feedback,
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
