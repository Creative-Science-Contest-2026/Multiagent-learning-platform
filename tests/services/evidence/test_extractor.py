from __future__ import annotations

from deeptutor.services.evidence.extractor import (
    extract_observations_from_review,
    extract_observations_from_tutoring_turn,
)


def test_extract_observations_from_review_builds_topic_level_signals() -> None:
    review = {
        "session_id": "quiz-1",
        "student_id": "student-a",
        "results": [
            {
                "question_id": "q1",
                "question": "Solve fractions subtraction 3/4 - 1/2",
                "is_correct": False,
                "duration_seconds": 48,
            },
            {
                "question_id": "q2",
                "question": "Solve fractions subtraction 5/6 - 1/3",
                "is_correct": False,
                "duration_seconds": 61,
            },
        ],
    }

    rows = extract_observations_from_review(review)

    assert len(rows) == 2
    assert rows[0]["student_id"] == "student-a"
    assert rows[0]["topic"] == "fractions subtraction"
    assert rows[0]["source"] == "assessment"
    assert rows[0]["is_correct"] is False
    assert rows[0]["latency_seconds"] == 48


def test_extract_observations_from_review_marks_dominant_error_for_repeated_misses() -> None:
    review = {
        "session_id": "quiz-2",
        "student_id": "student-b",
        "results": [
            {
                "question_id": "q1",
                "question": "Solve algebra equation 2x = 10",
                "is_correct": False,
                "duration_seconds": 20,
            },
            {
                "question_id": "q2",
                "question": "Solve algebra equation x + 2 = 5",
                "is_correct": False,
                "duration_seconds": 18,
            },
        ],
    }

    rows = extract_observations_from_review(review)

    assert {row["dominant_error"] for row in rows} == {"concept_gap"}


def test_extract_observations_from_tutoring_turn_uses_followup_context() -> None:
    rows = extract_observations_from_tutoring_turn(
        session_id="sess-1",
        student_id="student-1",
        user_message="I still don't get this",
        assistant_message="Let's break this down with one hint.",
        followup_question_context={
            "question_id": "q_3",
            "question": "What is 3/4 - 1/2?",
            "is_correct": False,
        },
        turn_events=[
            {"timestamp": 100.0},
            {"timestamp": 112.4},
        ],
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["source"] == "tutoring"
    assert row["question_id"] == "q_3"
    assert row["is_correct"] is False
    assert row["latency_seconds"] == 12
    assert row["hint_count"] >= 1
    assert row["retry_count"] >= 1
    assert row["dominant_error"] == "careless_error"


def test_extract_observations_from_tutoring_turn_defaults_to_non_regressive_correctness() -> None:
    rows = extract_observations_from_tutoring_turn(
        session_id="sess-2",
        student_id="student-2",
        user_message="Explain matrix rank",
        assistant_message="Matrix rank is the number of linearly independent columns.",
        followup_question_context=None,
        turn_events=None,
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["source"] == "tutoring"
    assert row["question_id"] == ""
    assert row["is_correct"] is True
    assert row["dominant_error"] is None
