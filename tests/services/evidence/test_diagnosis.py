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
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["recommended_actions"][0]["action_type"] == "review_prerequisite"
