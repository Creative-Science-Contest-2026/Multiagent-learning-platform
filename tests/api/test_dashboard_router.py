from __future__ import annotations

import sqlite3

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


def _set_session_timestamp(store: SQLiteSessionStore, session_id: str, timestamp: float) -> None:
    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "UPDATE sessions SET created_at = ?, updated_at = ? WHERE id = ?",
            (timestamp, timestamp, session_id),
        )
        conn.execute(
            "UPDATE turns SET created_at = ?, updated_at = ?, finished_at = ? WHERE session_id = ?",
            (timestamp, timestamp, timestamp, session_id),
        )
        conn.execute(
            "UPDATE messages SET created_at = ? WHERE session_id = ?",
            (timestamp, session_id),
        )
        conn.commit()


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


@pytest.mark.asyncio
async def test_dashboard_assessment_analysis_returns_topic_breakdown(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="analysis-session",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "analysis-session",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "2. [q2] Q: Solve algebra equation 2x = 10 -> Answered: 3 (Incorrect, correct: 5)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/assessment-analysis/analysis-session")

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == "analysis-session"
    assert payload["summary"]["score_percent"] == 50
    assert len(payload["performance_by_topic"]) >= 1
    assert "recommendations" in payload
    assert len(payload["recommendations"]) >= 1


@pytest.mark.asyncio
async def test_student_progress_summarizes_scores_topics_and_streak(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="assessment-recent",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "assessment-recent",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve fractions addition 1/2 + 1/4 -> Answered: 3/4 (Correct)\n"
        "2. [q2] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4)\n"
        "Score: 1/2 (50%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-recent", 1_710_000_000)

    await _seed_session(
        store,
        session_id="assessment-older",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "assessment-older",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct)\n"
        "2. [q2] Q: Solve algebra equation 2x = 10 -> Answered: 5 (Correct)\n"
        "Score: 2/2 (100%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-older", 1_709_913_600)

    await _seed_session(
        store,
        session_id="tutor-recent",
        capability="chat",
        message="Help me review fractions mistakes",
        knowledge_bases=["fractions-pack"],
    )
    _set_session_timestamp(store, "tutor-recent", 1_709_827_200)

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/dashboard/student-progress")

    assert response.status_code == 200
    payload = response.json()
    assert payload["totals"] == {
        "assessments_completed": 2,
        "tutoring_sessions": 1,
        "knowledge_packs_used": 2,
        "average_score_percent": 75,
        "streak_days": 3,
    }
    assert payload["focus_topics"][0]["topic"] == "fractions subtraction"
    assert payload["focus_topics"][0]["incorrect_count"] == 1
    assert payload["mastered_topics"][0]["topic"] == "algebra equation"
    assert payload["score_trend"] == [
        {"session_id": "assessment-older", "score_percent": 100, "timestamp": 1_709_913_600},
        {"session_id": "assessment-recent", "score_percent": 50, "timestamp": 1_710_000_000},
    ]
    assert [row["session_id"] for row in payload["recent_assessments"]] == [
        "assessment-recent",
        "assessment-older",
    ]
