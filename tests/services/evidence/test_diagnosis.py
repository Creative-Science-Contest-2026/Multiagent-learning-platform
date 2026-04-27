from __future__ import annotations

from deeptutor.services.evidence.diagnosis import build_student_diagnosis


def test_build_student_diagnosis_returns_structured_hypotheses_and_actions() -> None:
    observations = [
        {
            "observation_id": "obs_1",
            "session_id": "quiz-1",
            "student_id": "student-a",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 48,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
        {
            "observation_id": "obs_2",
            "session_id": "quiz-1",
            "student_id": "student-a",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q2",
            "is_correct": False,
            "latency_seconds": 61,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
    ]
    state = {
        "student_id": "student-a",
        "repeated_mistakes": ["fractions subtraction"],
        "support_level": "guided",
        "confidence_trend": "down",
        "mastery_signals": {
            "emerging_topics": ["fractions subtraction"],
            "stable_topics": [],
            "at_risk_topics": ["fractions subtraction"],
        },
        "support_signals": {
            "heavy_hint_topics": ["fractions subtraction"],
            "retry_heavy_topics": [],
            "recent_support_burden": "elevated",
        },
        "misconception_signals": {
            "dominant_errors": {"fractions subtraction": "concept_gap"},
            "persistent_topics": ["fractions subtraction"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-a",
        observations=observations,
        student_state=state,
    )

    assert payload["student_id"] == "student-a"
    assert payload["diagnosis_policy"] == "rule_assisted_teacher_review"
    assert payload["teacher_review_required"] is True
    assert payload["observed"]["topic"] == "fractions subtraction"
    assert payload["observed"]["abstained"] is False
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["inferred"][0]["confidence_tag"] in {"medium", "high"}
    assert "teacher-reviewable hypothesis" in payload["inferred"][0]["teacher_review_note"]
    assert payload["recommended_actions"][0]["action_type"] == "review_prerequisite"
    assert "Teacher should confirm" in payload["recommended_actions"][0]["teacher_review_note"]
    assert payload["student_state"]["mastery_signals"]["at_risk_topics"] == ["fractions subtraction"]
    assert payload["student_state"]["support_signals"]["recent_support_burden"] == "elevated"
    assert payload["student_state"]["misconception_signals"]["dominant_errors"]["fractions subtraction"] == "concept_gap"


def test_build_student_diagnosis_routes_careless_error_to_retry_action() -> None:
    observations = [
        {
            "observation_id": "obs_c1",
            "session_id": "quiz-2",
            "student_id": "student-c",
            "source": "assessment",
            "topic": "arithmetic",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 8,
            "hint_count": 0,
            "retry_count": 0,
            "dominant_error": "careless_error",
        },
        {
            "observation_id": "obs_c2",
            "session_id": "quiz-2",
            "student_id": "student-c",
            "source": "assessment",
            "topic": "arithmetic",
            "question_id": "q2",
            "is_correct": False,
            "latency_seconds": 10,
            "hint_count": 0,
            "retry_count": 0,
            "dominant_error": "careless_error",
        },
    ]

    payload = build_student_diagnosis(
        student_id="student-c",
        observations=observations,
        student_state=None,
    )

    assert payload["inferred"][0]["diagnosis_type"] == "careless_error"
    assert payload["recommended_actions"][0]["action_type"] == "retry_easier"
    assert payload["observed"]["abstain_reason"] == ""


def test_build_student_diagnosis_abstains_on_weak_or_non_error_signal() -> None:
    observations = [
        {
            "observation_id": "obs_ok",
            "session_id": "quiz-3",
            "student_id": "student-d",
            "source": "assessment",
            "topic": "geometry",
            "question_id": "q1",
            "is_correct": True,
            "latency_seconds": 20,
            "hint_count": 0,
            "retry_count": 0,
            "dominant_error": None,
        }
    ]

    payload = build_student_diagnosis(
        student_id="student-d",
        observations=observations,
        student_state=None,
    )

    assert payload["observed"]["abstained"] is True
    assert payload["observed"]["abstain_reason_code"] == "thin_evidence"
    assert payload["observed"]["abstain_reason"] == "Evidence is too weak or too mixed for a confident diagnosis."
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []


def test_build_student_diagnosis_abstains_on_mixed_signal() -> None:
    observations = [
        {
            "observation_id": "obs_m1",
            "session_id": "quiz-5",
            "student_id": "student-m",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 34,
            "hint_count": 0,
            "retry_count": 0,
            "dominant_error": None,
        },
        {
            "observation_id": "obs_m2",
            "session_id": "quiz-5",
            "student_id": "student-m",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q2",
            "is_correct": True,
            "latency_seconds": 45,
            "hint_count": 2,
            "retry_count": 1,
            "dominant_error": None,
        },
        {
            "observation_id": "obs_m3",
            "session_id": "quiz-5",
            "student_id": "student-m",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": "q3",
            "is_correct": True,
            "latency_seconds": 41,
            "hint_count": 2,
            "retry_count": 1,
            "dominant_error": None,
        },
    ]

    payload = build_student_diagnosis(
        student_id="student-m",
        observations=observations,
        student_state=None,
    )

    assert payload["observed"]["abstained"] is True
    assert payload["observed"]["abstain_reason_code"] == "mixed_evidence"
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []


def test_build_student_diagnosis_abstains_on_stale_evidence() -> None:
    observations = [
        {
            "observation_id": "obs_old1",
            "session_id": "quiz-6",
            "student_id": "student-old",
            "source": "assessment",
            "topic": "equations",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 52,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
        {
            "observation_id": "obs_old2",
            "session_id": "quiz-6",
            "student_id": "student-old",
            "source": "assessment",
            "topic": "equations",
            "question_id": "q2",
            "is_correct": False,
            "latency_seconds": 57,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        },
    ]
    stale_state = {
        "student_id": "student-old",
        "repeated_mistakes": ["equations"],
        "support_level": "guided",
        "confidence_trend": "down",
        "recency_summary": {
            "total_observations": 2,
            "window_size": 24,
            "bucket_counts": {
                "last_24h": 0,
                "last_7d": 0,
                "last_30d": 0,
                "older": 2,
            },
            "recent_incorrect": 2,
            "weighted_topic_misses": {
                "equations": 0.18,
            },
        },
        "mastery_signals": {
            "emerging_topics": [],
            "stable_topics": [],
            "at_risk_topics": ["equations"],
        },
        "support_signals": {
            "heavy_hint_topics": [],
            "retry_heavy_topics": [],
            "recent_support_burden": "steady",
        },
        "misconception_signals": {
            "dominant_errors": {"equations": "concept_gap"},
            "persistent_topics": ["equations"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-old",
        observations=observations,
        student_state=stale_state,
    )

    assert payload["observed"]["abstained"] is True
    assert payload["observed"]["abstain_reason_code"] == "stale_evidence"
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []


def test_build_student_diagnosis_keeps_enriched_student_state_as_context_only() -> None:
    observations = [
        {
            "observation_id": "obs_s1",
            "session_id": "quiz-4",
            "student_id": "student-e",
            "source": "assessment",
            "topic": "equations",
            "question_id": "q1",
            "is_correct": False,
            "latency_seconds": 32,
            "hint_count": 2,
            "retry_count": 0,
            "dominant_error": "needs_scaffold",
        },
        {
            "observation_id": "obs_s2",
            "session_id": "quiz-4",
            "student_id": "student-e",
            "source": "assessment",
            "topic": "equations",
            "question_id": "q2",
            "is_correct": False,
            "latency_seconds": 35,
            "hint_count": 2,
            "retry_count": 1,
            "dominant_error": "needs_scaffold",
        },
    ]
    enriched_state = {
        "student_id": "student-e",
        "repeated_mistakes": ["equations"],
        "support_level": "guided",
        "confidence_trend": "down",
        "mastery_signals": {
            "emerging_topics": [],
            "stable_topics": [],
            "at_risk_topics": ["equations"],
        },
        "support_signals": {
            "heavy_hint_topics": ["equations"],
            "retry_heavy_topics": [],
            "recent_support_burden": "elevated",
        },
        "misconception_signals": {
            "dominant_errors": {"equations": "needs_scaffold"},
            "persistent_topics": ["equations"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-e",
        observations=observations,
        student_state=enriched_state,
    )

    assert payload["observed"]["topic"] == "equations"
    assert payload["observed"]["abstained"] is False
    assert payload["observed"]["abstain_reason_code"] == ""
    assert payload["inferred"][0]["diagnosis_type"] == "needs_scaffold"
    assert payload["student_state"]["misconception_signals"]["persistent_topics"] == ["equations"]


def test_build_student_diagnosis_uses_high_confidence_for_recent_consistent_evidence() -> None:
    observations = [
        {
            "observation_id": f"obs_h{i}",
            "session_id": "quiz-7",
            "student_id": "student-high",
            "source": "assessment",
            "topic": "fractions subtraction",
            "question_id": f"q{i}",
            "is_correct": False,
            "latency_seconds": 52 + i,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        }
        for i in range(1, 5)
    ]
    state = {
        "student_id": "student-high",
        "repeated_mistakes": ["fractions subtraction"],
        "support_level": "guided",
        "confidence_trend": "down",
        "recency_summary": {
            "total_observations": 4,
            "window_size": 24,
            "bucket_counts": {
                "last_24h": 4,
                "last_7d": 0,
                "last_30d": 0,
                "older": 0,
            },
            "recent_incorrect": 4,
            "weighted_topic_misses": {"fractions subtraction": 3.5},
        },
        "mastery_signals": {
            "emerging_topics": [],
            "stable_topics": [],
            "at_risk_topics": ["fractions subtraction"],
        },
        "support_signals": {
            "heavy_hint_topics": [],
            "retry_heavy_topics": [],
            "recent_support_burden": "steady",
        },
        "misconception_signals": {
            "dominant_errors": {"fractions subtraction": "concept_gap"},
            "persistent_topics": ["fractions subtraction"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-high",
        observations=observations,
        student_state=state,
    )

    assert payload["observed"]["abstained"] is False
    assert payload["inferred"][0]["confidence_tag"] == "high"


def test_build_student_diagnosis_caps_confidence_when_support_burden_is_high() -> None:
    observations = [
        {
            "observation_id": f"obs_s{i}",
            "session_id": "quiz-8",
            "student_id": "student-support",
            "source": "assessment",
            "topic": "equations",
            "question_id": f"q{i}",
            "is_correct": False,
            "latency_seconds": 56 + i,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        }
        for i in range(1, 5)
    ]
    state = {
        "student_id": "student-support",
        "repeated_mistakes": ["equations"],
        "support_level": "guided",
        "confidence_trend": "down",
        "recency_summary": {
            "total_observations": 7,
            "window_size": 24,
            "bucket_counts": {
                "last_24h": 7,
                "last_7d": 0,
                "last_30d": 0,
                "older": 0,
            },
            "recent_incorrect": 4,
            "weighted_topic_misses": {"equations": 3.5},
        },
        "mastery_signals": {
            "emerging_topics": [],
            "stable_topics": [],
            "at_risk_topics": ["equations"],
        },
        "support_signals": {
            "heavy_hint_topics": ["equations"],
            "retry_heavy_topics": ["equations"],
            "recent_support_burden": "high",
        },
        "misconception_signals": {
            "dominant_errors": {"equations": "concept_gap"},
            "persistent_topics": ["equations"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-support",
        observations=observations,
        student_state=state,
    )

    assert payload["observed"]["abstained"] is False
    assert payload["inferred"][0]["confidence_tag"] == "medium"


def test_build_student_diagnosis_caps_confidence_when_evidence_is_not_recent() -> None:
    observations = [
        {
            "observation_id": f"obs_r{i}",
            "session_id": "quiz-9",
            "student_id": "student-recency",
            "source": "assessment",
            "topic": "decimals",
            "question_id": f"q{i}",
            "is_correct": False,
            "latency_seconds": 50 + i,
            "hint_count": 0,
            "retry_count": 1,
            "dominant_error": "concept_gap",
        }
        for i in range(1, 5)
    ]
    state = {
        "student_id": "student-recency",
        "repeated_mistakes": ["decimals"],
        "support_level": "guided",
        "confidence_trend": "down",
        "recency_summary": {
            "total_observations": 4,
            "window_size": 24,
            "bucket_counts": {
                "last_24h": 0,
                "last_7d": 4,
                "last_30d": 0,
                "older": 0,
            },
            "recent_incorrect": 4,
            "weighted_topic_misses": {"decimals": 2.1},
        },
        "mastery_signals": {
            "emerging_topics": [],
            "stable_topics": [],
            "at_risk_topics": ["decimals"],
        },
        "support_signals": {
            "heavy_hint_topics": [],
            "retry_heavy_topics": [],
            "recent_support_burden": "steady",
        },
        "misconception_signals": {
            "dominant_errors": {"decimals": "concept_gap"},
            "persistent_topics": ["decimals"],
        },
    }

    payload = build_student_diagnosis(
        student_id="student-recency",
        observations=observations,
        student_state=state,
    )

    assert payload["observed"]["abstained"] is False
    assert payload["inferred"][0]["confidence_tag"] == "medium"
