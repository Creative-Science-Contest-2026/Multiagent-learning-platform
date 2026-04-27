from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3
from typing import Any
from uuid import uuid4

_ALLOWED_LABELS = {"helpful", "wrong", "incomplete"}


def _now_ts() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def _connect(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table(db_path) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnosis_feedback (
                id TEXT PRIMARY KEY,
                student_id TEXT NOT NULL,
                source_topic TEXT NOT NULL,
                source_diagnosis_type TEXT NOT NULL,
                feedback_label TEXT NOT NULL,
                teacher_note TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_diagnosis_feedback_student
                ON diagnosis_feedback(student_id, updated_at DESC)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_diagnosis_feedback_source
                ON diagnosis_feedback(student_id, source_topic, source_diagnosis_type, updated_at DESC)
            """
        )
        conn.commit()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "student_id": row["student_id"],
        "source_topic": row["source_topic"],
        "source_diagnosis_type": row["source_diagnosis_type"],
        "feedback_label": row["feedback_label"],
        "teacher_note": row["teacher_note"],
        "created_at": int(row["created_at"]),
        "updated_at": int(row["updated_at"]),
    }


def list_diagnosis_feedback(store: Any) -> list[dict[str, Any]]:
    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, student_id, source_topic, source_diagnosis_type, feedback_label,
                   teacher_note, created_at, updated_at
            FROM diagnosis_feedback
            ORDER BY updated_at DESC, created_at DESC, id DESC
            """
        ).fetchall()
    return [_row_to_record(row) for row in rows]


def create_diagnosis_feedback(
    store: Any,
    *,
    student_id: str,
    source_topic: str,
    source_diagnosis_type: str,
    feedback_label: str,
    teacher_note: str = "",
) -> dict[str, Any]:
    if feedback_label not in _ALLOWED_LABELS:
        raise ValueError("invalid feedback_label")

    cleaned_student_id = student_id.strip()
    cleaned_topic = source_topic.strip()
    cleaned_type = source_diagnosis_type.strip()
    cleaned_note = teacher_note.strip()
    if not cleaned_student_id or not cleaned_topic or not cleaned_type:
        raise ValueError("missing required diagnosis feedback field")

    now = _now_ts()
    record = {
        "id": f"diagnosis-feedback:{uuid4().hex}",
        "student_id": cleaned_student_id,
        "source_topic": cleaned_topic,
        "source_diagnosis_type": cleaned_type,
        "feedback_label": feedback_label,
        "teacher_note": cleaned_note,
        "created_at": now,
        "updated_at": now,
    }

    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        conn.execute(
            """
            INSERT INTO diagnosis_feedback (
                id, student_id, source_topic, source_diagnosis_type, feedback_label,
                teacher_note, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["student_id"],
                record["source_topic"],
                record["source_diagnosis_type"],
                record["feedback_label"],
                record["teacher_note"],
                record["created_at"],
                record["updated_at"],
            ),
        )
        conn.commit()
    return deepcopy(record)


def update_diagnosis_feedback(
    store: Any,
    feedback_id: str,
    *,
    feedback_label: str,
    teacher_note: str | None = None,
) -> dict[str, Any]:
    if feedback_label not in _ALLOWED_LABELS:
        raise ValueError("invalid feedback_label")

    cleaned_note = teacher_note.strip() if teacher_note is not None else None
    _ensure_table(store.db_path)
    now = _now_ts()
    with _connect(store.db_path) as conn:
        row = conn.execute(
            """
            SELECT id, student_id, source_topic, source_diagnosis_type, feedback_label,
                   teacher_note, created_at, updated_at
            FROM diagnosis_feedback
            WHERE id = ?
            """,
            (feedback_id,),
        ).fetchone()
        if row is None:
            raise KeyError(feedback_id)

        next_note = cleaned_note if cleaned_note is not None else row["teacher_note"]
        conn.execute(
            """
            UPDATE diagnosis_feedback
            SET feedback_label = ?, teacher_note = ?, updated_at = ?
            WHERE id = ?
            """,
            (feedback_label, next_note, now, feedback_id),
        )
        conn.commit()

        updated = dict(_row_to_record(row))
        updated["feedback_label"] = feedback_label
        updated["teacher_note"] = next_note
        updated["updated_at"] = now
        return updated
