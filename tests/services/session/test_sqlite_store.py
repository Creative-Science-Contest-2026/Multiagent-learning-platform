from __future__ import annotations

import sqlite3
import time
from pathlib import Path

import pytest

from deeptutor.services.path_service import PathService
from deeptutor.services.session.sqlite_store import SQLiteSessionStore


def test_sqlite_store_defaults_to_data_user_chat_history_db(tmp_path: Path) -> None:
    service = PathService.get_instance()
    original_root = service._project_root
    original_user_dir = service._user_data_dir

    try:
        service._project_root = tmp_path
        service._user_data_dir = tmp_path / "data" / "user"

        store = SQLiteSessionStore()

        assert store.db_path == tmp_path / "data" / "user" / "chat_history.db"
        assert store.db_path.exists()
    finally:
        service._project_root = original_root
        service._user_data_dir = original_user_dir


def test_sqlite_store_migrates_legacy_chat_history_db(tmp_path: Path) -> None:
    service = PathService.get_instance()
    original_root = service._project_root
    original_user_dir = service._user_data_dir

    try:
        service._project_root = tmp_path
        service._user_data_dir = tmp_path / "data" / "user"
        legacy_db = tmp_path / "data" / "chat_history.db"
        legacy_db.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(legacy_db) as conn:
            conn.execute("CREATE TABLE legacy (id INTEGER PRIMARY KEY)")
            conn.commit()

        store = SQLiteSessionStore()

        assert store.db_path.exists()
        assert not legacy_db.exists()
    finally:
        service._project_root = original_root
        service._user_data_dir = original_user_dir


@pytest.mark.asyncio
async def test_sqlite_store_persists_observations_and_student_state(tmp_path: Path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    await store.save_observations(
        [
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
            }
        ]
    )
    await store.upsert_student_state(
        "student-a",
        {
            "student_id": "student-a",
            "repeated_mistakes": ["fractions subtraction"],
            "support_level": "guided",
            "confidence_trend": "down",
            "recency_summary": {"total_observations": 1},
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
        },
    )

    observations = await store.list_observations(student_id="student-a")
    state = await store.get_student_state("student-a")

    assert len(observations) == 1
    assert observations[0]["topic"] == "fractions subtraction"
    assert state is not None
    assert state["support_level"] == "guided"
    assert state["confidence_trend"] == "down"
    assert state["recency_summary"]["total_observations"] == 1
    assert state["mastery_signals"]["at_risk_topics"] == ["fractions subtraction"]
    assert state["support_signals"]["recent_support_burden"] == "elevated"
    assert state["misconception_signals"]["dominant_errors"]["fractions subtraction"] == "concept_gap"


@pytest.mark.asyncio
async def test_sqlite_store_builds_recency_aware_student_state_rollup(tmp_path: Path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    now = time.time()

    await store.save_observations(
        [
            {
                "observation_id": "obs_recent_1",
                "session_id": "sess-1",
                "student_id": "student-rollup",
                "source": "assessment",
                "topic": "fractions subtraction",
                "question_id": "q1",
                "is_correct": False,
                "latency_seconds": 28,
                "hint_count": 2,
                "retry_count": 1,
                "dominant_error": "needs_scaffold",
                "created_at": now - 600,
            },
            {
                "observation_id": "obs_recent_2",
                "session_id": "sess-1",
                "student_id": "student-rollup",
                "source": "tutoring",
                "topic": "fractions subtraction",
                "question_id": "q2",
                "is_correct": False,
                "latency_seconds": 35,
                "hint_count": 2,
                "retry_count": 2,
                "dominant_error": "needs_scaffold",
                "created_at": now - 1200,
            },
            {
                "observation_id": "obs_old",
                "session_id": "sess-1",
                "student_id": "student-rollup",
                "source": "assessment",
                "topic": "algebra equations",
                "question_id": "q3",
                "is_correct": False,
                "latency_seconds": 45,
                "hint_count": 1,
                "retry_count": 0,
                "dominant_error": "concept_gap",
                "created_at": now - (40 * 24 * 60 * 60),
            },
        ]
    )

    rollup = await store.build_student_state_rollup("student-rollup")

    assert rollup is not None
    assert rollup["repeated_mistakes"][0] == "fractions subtraction"
    assert rollup["support_level"] in {"guided", "intensive"}
    assert rollup["confidence_trend"] in {"up", "flat", "down"}
    assert rollup["recency_summary"]["total_observations"] == 3
    assert rollup["recency_summary"]["bucket_counts"]["last_24h"] >= 2
    assert rollup["mastery_signals"]["at_risk_topics"][0] == "fractions subtraction"
    assert "fractions subtraction" in rollup["support_signals"]["heavy_hint_topics"]
    assert rollup["support_signals"]["recent_support_burden"] in {"elevated", "high"}
    assert rollup["misconception_signals"]["dominant_errors"]["fractions subtraction"] == "needs_scaffold"
    assert "fractions subtraction" in rollup["misconception_signals"]["persistent_topics"]


@pytest.mark.asyncio
async def test_sqlite_store_persists_agent_spec_pin_in_session_preferences(tmp_path: Path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")
    session = await store.create_session(title="Pinned session")

    updated = await store.update_session_preferences(
        session["id"],
        {
            "agent_spec_pin": {
                "agent_spec_id": "fraction-coach",
                "version": 2,
                "updated_at": "2026-04-27T00:00:00Z",
            }
        },
    )

    detail = await store.get_session(session["id"])

    assert updated is True
    assert detail is not None
    assert detail["preferences"]["agent_spec_pin"] == {
        "agent_spec_id": "fraction-coach",
        "version": 2,
        "updated_at": "2026-04-27T00:00:00Z",
    }
