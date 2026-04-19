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


def test_reset_demo_data_creates_expected_kb_and_sessions(tmp_path: Path) -> None:
    result = reset_demo_data(tmp_path, api_base="http://localhost:8001")

    kb_root = tmp_path / "data" / "knowledge_bases"
    config = _read_json(kb_root / "kb_config.json")
    kb_entry = config["knowledge_bases"][DEMO_KB_ID]
    metadata = _read_json(kb_root / DEMO_KB_ID / "metadata.json")
    db_path = tmp_path / "data" / "user" / "chat_history.db"

    assert result["knowledge_pack"] == DEMO_KB_ID
    assert result["sessions"] == [ASSESSMENT_SESSION_ID, TUTOR_SESSION_ID]
    assert kb_entry["subject"] == "Mathematics"
    assert kb_entry["grade"] == "Grade 9"
    assert metadata["owner"] == "Contest Demo Teacher"
    assert (kb_root / DEMO_KB_ID / "llamaindex_storage").is_dir()
    assert _count_rows(db_path, "sessions") == 2
    assert _count_rows(db_path, "messages") == 4
    assert _count_rows(db_path, "turns") == 2


def test_reset_demo_data_is_idempotent(tmp_path: Path) -> None:
    first = reset_demo_data(tmp_path, api_base="http://127.0.0.1:8001")
    second = reset_demo_data(tmp_path, api_base="http://127.0.0.1:8001")

    db_path = tmp_path / "data" / "user" / "chat_history.db"
    config = _read_json(tmp_path / "data" / "knowledge_bases" / "kb_config.json")

    assert first["sessions"] == second["sessions"]
    assert list(config["knowledge_bases"]) == [DEMO_KB_ID]
    assert _count_rows(db_path, "sessions") == 2
    assert _count_rows(db_path, "messages") == 4
    assert _count_rows(db_path, "turns") == 2


def test_reset_demo_data_rejects_non_local_api_base(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="local API base"):
        reset_demo_data(tmp_path, api_base="https://example.com")

    assert not (tmp_path / "data").exists()
