from __future__ import annotations

from deeptutor.services.evidence.intervention_effectiveness import summarize_intervention_effectiveness


def test_summarize_intervention_effectiveness_marks_helpful_when_later_errors_drop() -> None:
    intervention = {
        "item_type": "teacher_action",
        "topic": "fractions subtraction",
        "timestamp": 100,
        "status": "planned",
    }
    observations = [
        {
            "topic": "fractions subtraction",
            "created_at": 90,
            "is_correct": False,
            "hint_count": 0,
            "retry_count": 1,
        },
        {
            "topic": "fractions subtraction",
            "created_at": 120,
            "is_correct": True,
            "hint_count": 0,
            "retry_count": 0,
        },
        {
            "topic": "fractions subtraction",
            "created_at": 130,
            "is_correct": True,
            "hint_count": 0,
            "retry_count": 0,
        },
    ]

    summary = summarize_intervention_effectiveness(intervention=intervention, observations=observations)

    assert summary["label"] == "appears_helpful"
    assert summary["followup_observation_count"] == 2


def test_summarize_intervention_effectiveness_returns_no_followup_signal_without_later_rows() -> None:
    intervention = {
        "item_type": "intervention_assignment",
        "topic": "fractions subtraction",
        "timestamp": 100,
        "status": "done",
    }
    observations = [
        {
            "topic": "fractions subtraction",
            "created_at": 90,
            "is_correct": False,
            "hint_count": 1,
            "retry_count": 1,
        }
    ]

    summary = summarize_intervention_effectiveness(intervention=intervention, observations=observations)

    assert summary["label"] == "no_followup_signal"
    assert summary["followup_observation_count"] == 0


def test_summarize_intervention_effectiveness_marks_mixed_when_followup_stays_support_heavy() -> None:
    intervention = {
        "item_type": "teacher_action",
        "topic": "fractions subtraction",
        "timestamp": 100,
        "status": "planned",
    }
    observations = [
        {
            "topic": "fractions subtraction",
            "created_at": 120,
            "is_correct": True,
            "hint_count": 2,
            "retry_count": 1,
        },
        {
            "topic": "fractions subtraction",
            "created_at": 130,
            "is_correct": False,
            "hint_count": 1,
            "retry_count": 1,
        },
    ]

    summary = summarize_intervention_effectiveness(intervention=intervention, observations=observations)

    assert summary["label"] == "mixed_or_unclear"
    assert summary["followup_observation_count"] == 2
