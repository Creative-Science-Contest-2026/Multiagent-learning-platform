from __future__ import annotations

from deeptutor.services.evidence.extractor import extract_observations_from_review


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
