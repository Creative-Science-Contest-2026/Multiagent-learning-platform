from __future__ import annotations

from typing import Any


DIAGNOSIS_TYPES = (
    "concept_gap",
    "needs_scaffold",
    "careless_error",
    "low_confidence",
    "procedure_breakdown",
    "support_dependency",
    "fluency_gap",
)


def _boost_scores_from_student_state(
    *,
    scores: dict[str, int],
    student_state: dict[str, Any] | None,
    topic: str,
) -> None:
    if not isinstance(student_state, dict):
        return

    repeated = {str(item) for item in (student_state.get("repeated_mistakes") or [])}
    support = student_state.get("support_signals")
    support = support if isinstance(support, dict) else {}
    heavy_hint_topics = {str(item) for item in (support.get("heavy_hint_topics") or [])}
    retry_heavy_topics = {str(item) for item in (support.get("retry_heavy_topics") or [])}
    burden = str(support.get("recent_support_burden") or "")

    misconception = student_state.get("misconception_signals")
    misconception = misconception if isinstance(misconception, dict) else {}
    dominant_errors = misconception.get("dominant_errors")
    dominant_errors = dominant_errors if isinstance(dominant_errors, dict) else {}
    dominant_error = str(dominant_errors.get(topic) or "").strip()

    if topic in retry_heavy_topics and topic in repeated:
        scores["procedure_breakdown"] += 6

    if topic in heavy_hint_topics and burden in {"elevated", "high"}:
        scores["support_dependency"] += 6

    if dominant_error in scores and dominant_error not in {"concept_gap", "needs_scaffold"}:
        scores[dominant_error] += 2


def diagnosis_scores(
    rows: list[dict[str, Any]],
    *,
    student_state: dict[str, Any] | None = None,
    topic: str | None = None,
) -> tuple[dict[str, int], int, float]:
    scores = {key: 0 for key in DIAGNOSIS_TYPES}
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

            if retry_count >= 2 and hint_count >= 1:
                scores["procedure_breakdown"] += 4

            if hint_count >= 2 and retry_count >= 1:
                scores["support_dependency"] += 3

            if latency_value is not None and latency_value <= 15:
                scores["careless_error"] += 3
            elif (
                latency_value is not None
                and latency_value >= 42
                and hint_count == 0
                and retry_count == 0
                and not dominant_error
            ):
                scores["fluency_gap"] += 3
            elif latency_value is not None and latency_value >= 45:
                scores["concept_gap"] += 2
            else:
                scores["low_confidence"] += 1
        else:
            if hint_count >= 2 or retry_count >= 2:
                scores["low_confidence"] += 2
                contradictions += 1
            if hint_count >= 2 and retry_count >= 1:
                scores["support_dependency"] += 3

        if dominant_error in scores:
            scores[dominant_error] += 2

    _boost_scores_from_student_state(
        scores=scores,
        student_state=student_state,
        topic=topic or str(rows[0].get("topic") or "general"),
    )

    contradiction_ratio = float(contradictions) / float(max(1, len(rows)))
    return scores, evidence_count, contradiction_ratio


def select_diagnosis(scores: dict[str, int]) -> tuple[str, int, int]:
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_type, top_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0
    return top_type, top_score, second_score
