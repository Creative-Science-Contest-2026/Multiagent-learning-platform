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
    }

    payload = build_student_diagnosis(
        student_id="student-a",
        observations=observations,
        student_state=state,
    )

    assert payload["student_id"] == "student-a"
    assert payload["observed"]["topic"] == "fractions subtraction"
    assert payload["observed"]["abstained"] is False
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["inferred"][0]["confidence_tag"] in {"medium", "high"}
    assert payload["recommended_actions"][0]["action_type"] == "review_prerequisite"


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
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []
