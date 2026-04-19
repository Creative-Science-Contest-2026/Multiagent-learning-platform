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
    from deeptutor.api.routers import dashboard

    app = FastAPI()
    app.include_router(dashboard.router, prefix="/api/v1/dashboard")
    monkeypatch.setattr(dashboard, "get_sqlite_session_store", lambda: store)
    return app


async def _seed_session(
    store: SQLiteSessionStore,
    *,
    session_id: str,
    capability: str,
    message: str,
    knowledge_bases: list[str],
    status: str = "completed",
) -> None:
    await store.create_session(session_id=session_id)
    await store.update_session_preferences(
        session_id,
        {
            "capability": capability,
            "tools": ["rag"] if knowledge_bases else [],
            "knowledge_bases": knowledge_bases,
            "language": "en",
        },
    )
    turn = await store.create_turn(session_id, capability=capability)
    await store.add_message(session_id, "user", message, capability=capability)
    await store.update_turn_status(turn["id"], status)


@pytest.mark.asyncio
async def test_dashboard_overview_groups_activity_and_knowledge_packs(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz on quadratic equations",
        knowledge_bases=["math-pack"],
    )
    await _seed_session(
        store,
        session_id="tutor-session",
        capability="chat",
        message="Help a student review linear functions",
        knowledge_bases=["math-pack"],
        status="running",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["totals"]["total_sessions"] == 2
    assert payload["totals"]["assessments"] == 1
    assert payload["totals"]["tutoring_sessions"] == 1
    assert payload["totals"]["running"] == 1
    assert payload["knowledge_packs"] == [{"name": "math-pack", "session_count": 2}]
    assert payload["recent_activity"][0]["knowledge_bases"] == ["math-pack"]
    assert payload["recent_activity"][0]["type"] in {"assessment", "tutoring"}


@pytest.mark.asyncio
async def test_dashboard_recent_filters_assessment_activity(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz",
        knowledge_bases=["math-pack"],
    )
    await _seed_session(
        store,
        session_id="chat-session",
        capability="chat",
        message="Tutor a student",
        knowledge_bases=["math-pack"],
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/recent?type=assessment")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == "quiz-session"
    assert payload[0]["type"] == "assessment"


@pytest.mark.asyncio
async def test_dashboard_overview_includes_assessment_summary(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="quiz-session",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "quiz-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: 1+1 -> Answered: 2 (Correct)\n"
        "Score: 1/1 (100%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/overview")

    assert response.status_code == 200
    payload = response.json()
    assessment_row = payload["recent_activity"][0]
    assert assessment_row["review_ref"] == "dashboard/assessments/quiz-session"
    assert assessment_row["assessment_summary"]["score_percent"] == 100
    assert assessment_row["assessment_summary"]["total_questions"] == 1
