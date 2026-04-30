from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from scripts.contest.reset_demo_data import (
    ASSESSMENT_SESSION_ID,
    DEMO_KB_ID,
    TUTOR_SESSION_ID,
    reset_demo_data,
)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _count_rows(db_path: Path, table: str) -> int:
    with sqlite3.connect(db_path) as conn:
        return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def _kb_entries(config: dict) -> dict:
    return config.get("knowledge_bases", {})


def test_reset_demo_data_creates_expected_kb_and_sessions(tmp_path: Path) -> None:
    result = reset_demo_data(tmp_path, api_base="http://localhost:8001")

    kb_root = tmp_path / "data" / "knowledge_bases"
    config = _read_json(kb_root / "kb_config.json")
    entries = _kb_entries(config)
    kb_entry = entries[DEMO_KB_ID]
    metadata = _read_json(kb_root / DEMO_KB_ID / "metadata.json")
    db_path = tmp_path / "data" / "user" / "chat_history.db"
    shareable = [
        row for row in entries.values() if row.get("sharing_status") in {"public", "team"}
    ]
    imported = [
        name for name, row in entries.items() if name.endswith("__imported") and row.get("sharing_status") == "private"
    ]

    assert result["knowledge_pack"] == DEMO_KB_ID
    assert ASSESSMENT_SESSION_ID in result["sessions"]
    assert TUTOR_SESSION_ID in result["sessions"]
    assert kb_entry["subject"] == "Mathematics"
    assert kb_entry["grade"] == "Grade 9"
    assert metadata["owner"] == "Contest Demo Teacher"
    assert (kb_root / DEMO_KB_ID / "llamaindex_storage").is_dir()
    assert len(shareable) >= 6
    assert len(imported) >= 2
    assert _count_rows(db_path, "sessions") >= 10
    assert _count_rows(db_path, "messages") >= 30
    assert _count_rows(db_path, "turns") >= 10
    assert _count_rows(db_path, "observations") >= 12
    assert _count_rows(db_path, "student_states") >= 4
    assert _count_rows(db_path, "teacher_actions") >= 2
    assert _count_rows(db_path, "recommendation_acks") >= 2
    assert _count_rows(db_path, "recommendation_feedback") >= 2
    assert _count_rows(db_path, "teacher_overrides") >= 1
    assert _count_rows(db_path, "diagnosis_feedback") >= 2
    assert _count_rows(db_path, "intervention_assignments") >= 2


def test_reset_demo_data_is_idempotent(tmp_path: Path) -> None:
    first = reset_demo_data(tmp_path, api_base="http://127.0.0.1:8001")
    second = reset_demo_data(tmp_path, api_base="http://127.0.0.1:8001")

    db_path = tmp_path / "data" / "user" / "chat_history.db"
    config = _read_json(tmp_path / "data" / "knowledge_bases" / "kb_config.json")
    entries = _kb_entries(config)

    assert first["sessions"] == second["sessions"]
    assert first["knowledge_pack"] == second["knowledge_pack"] == DEMO_KB_ID
    assert len(entries) >= 8
    assert _count_rows(db_path, "sessions") >= 10
    assert _count_rows(db_path, "messages") >= 30
    assert _count_rows(db_path, "turns") >= 10
    assert _count_rows(db_path, "observations") >= 12
    assert _count_rows(db_path, "student_states") >= 4
    assert _count_rows(db_path, "teacher_actions") >= 2
    assert _count_rows(db_path, "intervention_assignments") >= 2


def test_reset_demo_data_rejects_non_local_api_base(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="local API base"):
        reset_demo_data(tmp_path, api_base="https://example.com")

    assert not (tmp_path / "data").exists()
