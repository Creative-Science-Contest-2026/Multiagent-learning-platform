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
    from deeptutor.api.routers import assessment

    app = FastAPI()
    app.include_router(assessment.router, prefix="/api/v1/assessment")
    monkeypatch.setattr(assessment, "get_sqlite_session_store", lambda: store)
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
async def test_assessment_recommend_returns_targeted_next_topic(
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
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4, time: 48s)\n"
        "2. [q2] Q: Solve fractions subtraction 5/6 - 1/3 -> Answered: 1/2 (Incorrect, correct: 1/2, time: 61s)\n"
        "Score: 0/2 (0%)",
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

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.post(
            "/api/v1/assessment/recommend",
            json={"session_id": "assessment-recent", "limit": 10},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["recommended_topic"] == "fractions subtraction"
    assert payload["suggested_action"] == "retry-focused-quiz"
    assert payload["recommended_knowledge_bases"] == ["fractions-pack"]
    assert payload["source_session_ids"] == ["assessment-recent", "assessment-older"]
    assert payload["history_summary"]["assessments_considered"] == 2
    assert payload["history_summary"]["average_score_percent"] == 50
    assert "fractions subtraction" in payload["reason"]


@pytest.mark.asyncio
async def test_assessment_recommend_returns_clean_empty_state_without_reviews(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="chat-only",
        capability="chat",
        message="Help me study geometry",
        knowledge_bases=["geometry-pack"],
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.post("/api/v1/assessment/recommend", json={})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "insufficient-data"
    assert payload["recommended_topic"] is None
    assert payload["suggested_action"] == "complete-assessment"
    assert payload["history_summary"]["assessments_considered"] == 0


@pytest.mark.asyncio
async def test_assessment_diagnosis_endpoint_returns_structured_payload(
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
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4, time: 48s)\n"
        "2. [q2] Q: Solve fractions subtraction 5/6 - 1/3 -> Answered: 1/6 (Incorrect, correct: 1/2, time: 61s)\n"
        "Score: 0/2 (0%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/assessment/diagnosis/assessment-recent")

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_id"] == "assessment-recent"
    assert payload["inferred"][0]["diagnosis_type"] == "concept_gap"
    assert payload["inferred"][0]["confidence_tag"] in {"medium", "high"}
    assert payload["observed"]["abstained"] is False
    assert payload["recommended_actions"][0]["topic"] == "fractions subtraction"


@pytest.mark.asyncio
async def test_assessment_diagnosis_endpoint_can_abstain_on_strong_correct_signal(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="assessment-perfect",
        capability="deep_question",
        message="Generate a quiz on algebra",
        knowledge_bases=["algebra-pack"],
    )
    await store.add_message(
        "assessment-perfect",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve algebra equation x + 2 = 5 -> Answered: 3 (Correct, time: 12s)\n"
        "Score: 1/1 (100%)",
        capability="deep_question",
    )

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/assessment/diagnosis/assessment-perfect")

    assert response.status_code == 200
    payload = response.json()
    assert payload["observed"]["abstained"] is True
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []


@pytest.mark.asyncio
async def test_assessment_diagnosis_endpoint_abstains_on_stale_evidence(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    await _seed_session(
        store,
        session_id="assessment-stale",
        capability="deep_question",
        message="Generate a quiz on fractions",
        knowledge_bases=["fractions-pack"],
    )
    await store.add_message(
        "assessment-stale",
        "user",
        "[Quiz Performance]\n"
        "1. [q1] Q: Solve fractions subtraction 3/4 - 1/2 -> Answered: 1/5 (Incorrect, correct: 1/4, time: 48s)\n"
        "2. [q2] Q: Solve fractions subtraction 5/6 - 1/3 -> Answered: 1/6 (Incorrect, correct: 1/2, time: 61s)\n"
        "Score: 0/2 (0%)",
        capability="deep_question",
    )
    _set_session_timestamp(store, "assessment-stale", 1_700_000_000)

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/assessment/diagnosis/assessment-stale")

    assert response.status_code == 200
    payload = response.json()
    assert payload["observed"]["abstained"] is True
    assert payload["observed"]["abstain_reason_code"] == "stale_evidence"
    assert payload["inferred"] == []
    assert payload["recommended_actions"] == []
