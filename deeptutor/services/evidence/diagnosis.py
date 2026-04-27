from __future__ import annotations

from typing import Any

from .confidence_calibration import calibrate_confidence_tag
from .evidence_sufficiency import classify_evidence_sufficiency

ACTION_BY_DIAGNOSIS = {
    "concept_gap": "review_prerequisite",
    "needs_scaffold": "increase_scaffold",
    "careless_error": "retry_easier",
    "low_confidence": "small_group_support",
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


def _diagnosis_scores(rows: list[dict[str, Any]]) -> tuple[dict[str, int], int, float]:
    scores = {
        "concept_gap": 0,
        "needs_scaffold": 0,
        "careless_error": 0,
        "low_confidence": 0,
    }
    contradictions = 0
    evidence_count = 0

    for row in rows:
        is_correct = bool(row.get("is_correct"))
        hint_count = int(row.get("hint_count") or 0)
        retry_count = int(row.get("retry_count") or 0)
        latency = row.get("latency_seconds")
        latency_value = int(latency) if latency is not None else None
        dominant_error = str(row.get("dominant_error") or "").strip()

        if not is_correct:
            evidence_count += 1
            scores["needs_scaffold"] += 1
            if hint_count >= 2 or retry_count >= 2:
                scores["needs_scaffold"] += 2
            if retry_count >= 1 and hint_count >= 1:
                scores["concept_gap"] += 1
            if latency_value is not None and latency_value <= 15:
                scores["careless_error"] += 3
            elif latency_value is not None and latency_value >= 45:
                scores["concept_gap"] += 2
            else:
                scores["low_confidence"] += 1
        else:
            # Correct-but-heavy-support patterns can still indicate low confidence.
            if hint_count >= 2 or retry_count >= 2:
                scores["low_confidence"] += 2
                contradictions += 1

        if dominant_error in scores:
            scores[dominant_error] += 2

    # Contradiction means mixed signals where dominant hypothesis is weaker.
    contradiction_ratio = float(contradictions) / float(max(1, len(rows)))
    return scores, evidence_count, contradiction_ratio


def _select_diagnosis(scores: dict[str, int]) -> tuple[str, int, int]:
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_type, top_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0
    return top_type, top_score, second_score


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
    scores, evidence_count, contradiction_ratio = _diagnosis_scores(dominant_rows)
    dominant_error, _top_score, _second_score = _select_diagnosis(scores)
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
