from __future__ import annotations

from typing import Any


def _base_confidence_tag(
    *,
    evidence_count: int,
    contradiction_ratio: float,
) -> str:
    if evidence_count >= 4 and contradiction_ratio <= 0.25:
        return "high"
    if evidence_count >= 2 and contradiction_ratio <= 0.45:
        return "medium"
    return "low"


def _recent_support_burden(student_state: dict[str, Any] | None) -> str:
    if not isinstance(student_state, dict):
        return ""
    support = student_state.get("support_signals")
    if not isinstance(support, dict):
        return ""
    return str(support.get("recent_support_burden") or "").strip()


def _last_24h_count(student_state: dict[str, Any] | None) -> int:
    if not isinstance(student_state, dict):
        return 0
    recency = student_state.get("recency_summary")
    if not isinstance(recency, dict):
        return 0
    buckets = recency.get("bucket_counts")
    if not isinstance(buckets, dict):
        return 0
    return int(buckets.get("last_24h") or 0)


def calibrate_confidence_tag(
    *,
    student_state: dict[str, Any] | None,
    evidence_count: int,
    contradiction_ratio: float,
) -> str:
    tag = _base_confidence_tag(
        evidence_count=evidence_count,
        contradiction_ratio=contradiction_ratio,
    )

    support_burden = _recent_support_burden(student_state)
    if support_burden in {"elevated", "high"} and tag == "high":
        tag = "medium"

    if tag == "high" and _last_24h_count(student_state) <= 0:
        tag = "medium"

    return tag
