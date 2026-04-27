from __future__ import annotations

from typing import Any


GENERIC_ABSTAIN_REASON = "Evidence is too weak or too mixed for a confident diagnosis."
STALE_ABSTAIN_REASON = "Evidence is stale and should be refreshed before making a recommendation."


def _is_stale_student_state(student_state: dict[str, Any] | None) -> bool:
    if not isinstance(student_state, dict):
        return False
    recency = student_state.get("recency_summary")
    if not isinstance(recency, dict):
        return False
    buckets = recency.get("bucket_counts")
    if not isinstance(buckets, dict):
        return False

    return (
        int(buckets.get("older") or 0) > 0
        and int(buckets.get("last_24h") or 0) == 0
        and int(buckets.get("last_7d") or 0) == 0
        and int(buckets.get("last_30d") or 0) == 0
    )


def classify_evidence_sufficiency(
    *,
    student_state: dict[str, Any] | None,
    miss_count: int,
    evidence_count: int,
    contradiction_ratio: float,
) -> tuple[bool, str, str]:
    if _is_stale_student_state(student_state):
        return False, "stale_evidence", STALE_ABSTAIN_REASON
    if miss_count == 0:
        return False, "thin_evidence", GENERIC_ABSTAIN_REASON
    if evidence_count <= 1 and contradiction_ratio >= 0.5:
        return False, "mixed_evidence", GENERIC_ABSTAIN_REASON
    return True, "", ""
