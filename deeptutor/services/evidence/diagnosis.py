from __future__ import annotations

from typing import Any

from .confidence_calibration import calibrate_confidence_tag
from .diagnosis_taxonomy import diagnosis_scores, select_diagnosis
from .evidence_sufficiency import classify_evidence_sufficiency

ACTION_BY_DIAGNOSIS = {
    "concept_gap": "review_prerequisite",
    "needs_scaffold": "increase_scaffold",
    "careless_error": "retry_easier",
    "low_confidence": "small_group_support",
    "procedure_breakdown": "increase_scaffold",
    "support_dependency": "small_group_support",
    "fluency_gap": "retry_easier",
}

ACTION_PRIORITY = {
    "review_prerequisite": 0,
    "increase_scaffold": 1,
    "retry_easier": 2,
    "small_group_support": 3,
}

DIAGNOSIS_POLICY = "rule_assisted_teacher_review"


def _support_level(observations: list[dict[str, Any]]) -> str:
    if any((row.get("hint_count") or 0) >= 2 for row in observations):
        return "intensive"
    if any(not row.get("is_correct") for row in observations):
        return "guided"
    return "independent"


def _topic_rows(observations: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    by_topic: dict[str, list[dict[str, Any]]] = {}
    for row in observations:
        topic = str(row.get("topic") or "general")
        by_topic.setdefault(topic, []).append(row)

    best_topic = "general"
    best_rows: list[dict[str, Any]] = observations
    best_score = float("-inf")
    for topic, rows in by_topic.items():
        miss_count = sum(1 for row in rows if not row.get("is_correct"))
        support_load = sum(
            int(row.get("hint_count") or 0) + int(row.get("retry_count") or 0)
            for row in rows
        )
        score = miss_count * 3 + support_load
        if score > best_score or (score == best_score and topic < best_topic):
            best_topic = topic
            best_rows = rows
            best_score = score
    return best_topic, best_rows

def _build_ranked_actions(
    *,
    student_id: str,
    topic: str,
    diagnosis_type: str,
    confidence_tag: str,
    miss_count: int,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    primary_action = ACTION_BY_DIAGNOSIS.get(diagnosis_type, "increase_scaffold")
    candidates.append(
        {
            "action_type": primary_action,
            "score": 4 if confidence_tag == "high" else 3 if confidence_tag == "medium" else 2,
            "rationale": f"Primary support for {topic} based on {diagnosis_type} pattern.",
        }
    )
    if miss_count >= 2 and diagnosis_type != "review_prerequisite":
        candidates.append(
            {
                "action_type": "review_prerequisite",
                "score": 2,
                "rationale": f"Multiple misses suggest prerequisite review for {topic}.",
            }
        )
    if diagnosis_type == "careless_error":
        candidates.append(
            {
                "action_type": "retry_easier",
                "score": 2,
                "rationale": f"Quick retry cycle can stabilize accuracy on {topic}.",
            }
        )

    ranked = sorted(
        candidates,
        key=lambda item: (-item["score"], ACTION_PRIORITY.get(item["action_type"], 99), item["action_type"]),
    )
    deduped: list[dict[str, Any]] = []
    seen_types: set[str] = set()
    for item in ranked:
        action_type = item["action_type"]
        if action_type in seen_types:
            continue
        seen_types.add(action_type)
        deduped.append(
            {
                "action_id": f"{student_id}:{topic}:{action_type}",
                "action_type": action_type,
                "target_student_ids": [student_id],
                "topic": topic,
                "rationale": item["rationale"],
                "teacher_review_note": (
                    f"Teacher should confirm that {action_type} matches the student's actual misconception before intervention."
                ),
            }
        )
    return deduped


def build_student_diagnosis(
    *,
    student_id: str,
    observations: list[dict[str, Any]],
    student_state: dict[str, Any] | None,
) -> dict[str, Any]:
    if not observations:
        return {
            "student_id": student_id,
            "diagnosis_policy": DIAGNOSIS_POLICY,
            "teacher_review_required": True,
            "observed": None,
            "student_state": student_state,
            "inferred": [],
            "recommended_actions": [],
        }

    dominant_topic, dominant_rows = _topic_rows(observations)
    scores, evidence_count, contradiction_ratio = diagnosis_scores(
        dominant_rows,
        student_state=student_state,
        topic=dominant_topic,
    )
    dominant_error, _top_score, _second_score = select_diagnosis(scores)
    confidence = calibrate_confidence_tag(
        student_state=student_state,
        evidence_count=evidence_count,
        contradiction_ratio=contradiction_ratio,
    )
    avg_latency_values = [
        int(row.get("latency_seconds") or 0)
        for row in dominant_rows
        if row.get("latency_seconds") is not None
    ]
    miss_count = sum(1 for row in dominant_rows if not row.get("is_correct"))
    evidence_sufficient, abstain_reason_code, abstain_reason = classify_evidence_sufficiency(
        student_state=student_state,
        miss_count=miss_count,
        evidence_count=evidence_count,
        contradiction_ratio=contradiction_ratio,
    )
    abstain = not evidence_sufficient

    derived_state = student_state or {
        "student_id": student_id,
        "repeated_mistakes": [dominant_topic],
        "support_level": _support_level(dominant_rows),
        "confidence_trend": "down",
    }

    inferred: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    if not abstain:
        inferred = [
            {
                "diagnosis_type": dominant_error,
                "confidence_tag": confidence,
                "topic": dominant_topic,
                "evidence": [
                    f"miss_count={miss_count} on {dominant_topic}",
                    f"support_level={_support_level(dominant_rows)}",
                    f"contradiction_ratio={round(contradiction_ratio, 2)}",
                ],
                "teacher_review_note": (
                    "Use this diagnosis as a teacher-reviewable hypothesis grounded in observed signals, not as an autonomous final judgment."
                ),
            }
        ]
        actions = _build_ranked_actions(
            student_id=student_id,
            topic=dominant_topic,
            diagnosis_type=dominant_error,
            confidence_tag=confidence,
            miss_count=miss_count,
        )

    return {
        "student_id": student_id,
        "diagnosis_policy": DIAGNOSIS_POLICY,
        "teacher_review_required": True,
        "observed": {
            "topic": dominant_topic,
            "miss_count": miss_count,
            "evidence_count": evidence_count,
            "abstained": abstain,
            "abstain_reason_code": abstain_reason_code,
            "abstain_reason": abstain_reason,
            "avg_latency_seconds": round(sum(avg_latency_values) / len(avg_latency_values))
            if avg_latency_values
            else 0,
        },
        "student_state": derived_state,
        "inferred": inferred,
        "recommended_actions": actions,
    }
