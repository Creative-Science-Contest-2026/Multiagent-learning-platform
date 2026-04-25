from __future__ import annotations

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency in lightweight envs
    FastAPI = None
    TestClient = None

from deeptutor.services.session.sqlite_store import SQLiteSessionStore

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(store: SQLiteSessionStore, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import sessions

    app = FastAPI()
    app.include_router(sessions.router, prefix="/api/v1/sessions")
    monkeypatch.setattr(sessions, "get_sqlite_session_store", lambda: store)
    return app


@pytest.mark.asyncio
async def test_get_assessment_review_returns_structured_score(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="quiz-review-session")
    await store.update_session_preferences(
        "quiz-review-session",
        {
            "capability": "deep_question",
            "tools": ["rag"],
            "knowledge_bases": ["math-pack"],
            "language": "en",
        },
    )
    await store.add_message(
        "quiz-review-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: 2+2 -> Answered: 4 (Correct)\n"
        "2. [q2] Q: 5-1 -> Answered: 3 (Incorrect, correct: 4)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/sessions/quiz-review-session/assessment-review")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "quiz-review-session"
    assert payload["knowledge_bases"] == ["math-pack"]
    assert payload["summary"]["total_questions"] == 2
    assert payload["summary"]["correct_count"] == 1
    assert payload["summary"]["incorrect_count"] == 1
    assert payload["summary"]["score_percent"] == 50
    assert payload["results"][0]["question_id"] == "q1"


@pytest.mark.asyncio
async def test_record_and_review_quiz_results_preserves_duration_metrics(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="quiz-duration-session")

    with TestClient(_build_app(store, monkeypatch)) as client:
        record_response = client.post(
            "/api/v1/sessions/quiz-duration-session/quiz-results",
            json={
                "answers": [
                    {
                        "question_id": "q1",
                        "question": "2+2",
                        "user_answer": "4",
                        "correct_answer": "4",
                        "is_correct": True,
                        "duration_seconds": 35,
                    },
                    {
                        "question_id": "q2",
                        "question": "5-1",
                        "user_answer": "3",
                        "correct_answer": "4",
                        "is_correct": False,
                        "duration_seconds": 65,
                    },
                ]
            },
        )

        review_response = client.get("/api/v1/sessions/quiz-duration-session/assessment-review")

    assert record_response.status_code == 200
    record_payload = record_response.json()
    assert "time: 35s" in record_payload["content"]
    assert "time: 65s" in record_payload["content"]

    assert review_response.status_code == 200
    review_payload = review_response.json()
    assert review_payload["summary"]["estimated_time_spent"] == 100
    assert review_payload["summary"]["average_time_per_question"] == 50
    assert review_payload["results"][0]["duration_seconds"] == 35
    assert review_payload["results"][1]["duration_seconds"] == 65


@pytest.mark.asyncio
async def test_assessment_review_includes_context_support_and_followups(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="quiz-context-session")
    await store.update_session_preferences(
        "quiz-context-session",
        {
            "capability": "deep_question",
            "tools": ["rag"],
            "knowledge_bases": ["fractions-pack"],
            "language": "en",
        },
    )
    await store.add_message(
        "quiz-context-session",
        "assistant",
        "Let's review what went wrong on fractions subtraction.",
        capability="chat",
        events=[
            {
                "type": "result",
                "metadata": {
                    "followup_questions": [
                        "Which subtraction step caused the mistake?",
                        "What common denominator should you use first?",
                    ],
                    "session_context": {
                        "knowledge_bases": ["fractions-pack"],
                        "followup_questions": [
                            "Which subtraction step caused the mistake?",
                            "What common denominator should you use first?",
                        ],
                    },
                },
            }
        ],
    )
    await store.add_message(
        "quiz-context-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4)\n"
        "Score: 0/1 (0%)",
        capability="deep_question",
    )
    await store.update_summary(
        "quiz-context-session",
        "Learner needs help with fraction subtraction and denominator alignment.",
        up_to_msg_id=2,
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/sessions/quiz-context-session/assessment-review")

    assert response.status_code == 200
    payload = response.json()
    assert payload["context_support"]["knowledge_bases"] == ["fractions-pack"]
    assert "fraction subtraction" in payload["context_support"]["conversation_summary"].lower()
    assert payload["context_support"]["followup_questions"] == [
        "Which subtraction step caused the mistake?",
        "What common denominator should you use first?",
    ]
    assert payload["context_support"]["incorrect_questions"] == [
        {
            "question_id": "q1",
            "question": "3/4 - 1/2",
            "correct_answer": "1/4",
        }
    ]


@pytest.mark.asyncio
async def test_get_session_includes_context_support_snapshot(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await store.create_session(session_id="chat-context-session")
    await store.update_session_preferences(
        "chat-context-session",
        {
            "capability": "chat",
            "tools": ["rag"],
            "knowledge_bases": ["biology-pack"],
            "language": "en",
        },
    )
    await store.add_message(
        "chat-context-session",
        "user",
        "Why do plants need sunlight?",
        capability="chat",
    )
    await store.add_message(
        "chat-context-session",
        "assistant",
        "Plants use sunlight to drive photosynthesis.",
        capability="chat",
        events=[
            {
                "type": "result",
                "metadata": {
                    "session_context": {
                        "followup_questions": [
                            "What role does chlorophyll play?",
                        ]
                    }
                },
            }
        ],
    )
    await store.update_summary(
        "chat-context-session",
        "Learner is reviewing basic photosynthesis concepts.",
        up_to_msg_id=2,
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/sessions/chat-context-session")

    assert response.status_code == 200
    payload = response.json()
    assert payload["context_support"]["knowledge_bases"] == ["biology-pack"]
    assert payload["context_support"]["last_user_message"] == "Why do plants need sunlight?"
    assert payload["context_support"]["last_assistant_message"] == "Plants use sunlight to drive photosynthesis."
    assert payload["context_support"]["followup_questions"] == ["What role does chlorophyll play?"]
