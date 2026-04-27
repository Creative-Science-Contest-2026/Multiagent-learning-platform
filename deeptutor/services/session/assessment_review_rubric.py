from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any


def _ensure_table(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assessment_rubric_reviews (
                session_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL
            )
            """
        )
        conn.commit()


def get_assessment_rubric_review(db_path: Path, session_id: str) -> dict[str, Any] | None:
    _ensure_table(db_path)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT payload_json FROM assessment_rubric_reviews WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    return json.loads(row[0])


def upsert_assessment_rubric_review(
    db_path: Path,
    session_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    _ensure_table(db_path)
    existing = get_assessment_rubric_review(db_path, session_id)
    now = int(time.time())
    record = {
        "id": existing["id"] if existing else str(uuid.uuid4()),
        "session_id": session_id,
        "wording_quality": payload["wording_quality"],
        "distractor_quality": payload["distractor_quality"],
        "explanation_clarity": payload["explanation_clarity"],
        "overall_decision": payload["overall_decision"],
        "teacher_note": str(payload.get("teacher_note") or ""),
        "created_at": existing["created_at"] if existing else now,
        "updated_at": now,
    }
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "REPLACE INTO assessment_rubric_reviews (session_id, payload_json) VALUES (?, ?)",
            (session_id, json.dumps(record, ensure_ascii=False)),
        )
        conn.commit()
    return record
