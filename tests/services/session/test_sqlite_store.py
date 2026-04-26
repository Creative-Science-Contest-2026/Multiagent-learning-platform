from __future__ import annotations

import sqlite3
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
        },
    )

    observations = await store.list_observations(student_id="student-a")
    state = await store.get_student_state("student-a")

    assert len(observations) == 1
    assert observations[0]["topic"] == "fractions subtraction"
    assert state is not None
    assert state["support_level"] == "guided"
    assert state["confidence_trend"] == "down"
