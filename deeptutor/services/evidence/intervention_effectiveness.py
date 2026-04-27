from __future__ import annotations

from typing import Any


def summarize_intervention_effectiveness(
    *,
    intervention: dict[str, Any],
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    topic = str(intervention.get("topic") or "").strip()
    anchor_ts = int(intervention.get("timestamp") or 0)
    if not topic or anchor_ts <= 0:
        return {
            "label": "no_followup_signal",
            "reason": "Intervention record lacks enough context for a follow-up check.",
            "followup_observation_count": 0,
        }

    followup_rows = [
        row
        for row in observations
        if str(row.get("topic") or "").strip() == topic and float(row.get("created_at") or 0) > float(anchor_ts)
    ]
    followup_rows.sort(key=lambda row: float(row.get("created_at") or 0))
    if not followup_rows:
        return {
            "label": "no_followup_signal",
            "reason": "No later same-topic observations were recorded after this intervention.",
            "followup_observation_count": 0,
        }

    recent_rows = followup_rows[-2:]
    if len(recent_rows) >= 2 and all(
        bool(row.get("is_correct"))
        and int(row.get("hint_count") or 0) == 0
        and int(row.get("retry_count") or 0) == 0
        for row in recent_rows
    ):
        return {
            "label": "appears_helpful",
            "reason": "The most recent same-topic follow-up observations were correct without added support.",
            "followup_observation_count": len(recent_rows),
        }

    return {
        "label": "mixed_or_unclear",
        "reason": "Later same-topic observations exist, but the pattern is still mixed or support-heavy.",
        "followup_observation_count": len(followup_rows),
    }
