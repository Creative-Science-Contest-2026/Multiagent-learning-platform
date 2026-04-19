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
