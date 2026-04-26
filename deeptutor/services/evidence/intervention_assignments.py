from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3
from typing import Any
from uuid import uuid4

_ALLOWED_ASSIGNMENT_TYPES = {
    "practice_set",
    "reteach_session",
    "prerequisite_review",
    "small_group_activity",
}
_ALLOWED_ASSIGNMENT_STATUSES = {"draft", "planned", "done", "dismissed"}


def _now_ts() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp())


def _connect(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_tables(db_path) -> None:
    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS intervention_assignments (
                id TEXT PRIMARY KEY,
                teacher_action_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                assignment_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                teacher_note TEXT NOT NULL,
                practice_note TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_intervention_assignments_target
                ON intervention_assignments(target_type, target_id, updated_at DESC)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_intervention_assignments_action
                ON intervention_assignments(teacher_action_id, updated_at DESC)
            """
        )
        conn.commit()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "teacher_action_id": row["teacher_action_id"],
        "target_type": row["target_type"],
        "target_id": row["target_id"],
        "assignment_type": row["assignment_type"],
        "topic": row["topic"],
        "title": row["title"],
        "teacher_note": row["teacher_note"],
        "practice_note": row["practice_note"],
        "status": row["status"],
        "created_at": int(row["created_at"]),
        "updated_at": int(row["updated_at"]),
    }


def list_intervention_assignments(store: Any) -> list[dict[str, Any]]:
    _ensure_tables(store.db_path)
    with _connect(store.db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, teacher_action_id, target_type, target_id, assignment_type,
                   topic, title, teacher_note, practice_note, status, created_at, updated_at
            FROM intervention_assignments
            ORDER BY updated_at DESC, created_at DESC, id DESC
            """
        ).fetchall()
    return [_row_to_record(row) for row in rows]


def create_intervention_assignment(
    store: Any,
    *,
    teacher_action_id: str,
    assignment_type: str,
    title: str,
    teacher_note: str,
    practice_note: str,
) -> dict[str, Any]:
    if assignment_type not in _ALLOWED_ASSIGNMENT_TYPES:
        raise ValueError("invalid assignment_type")

    cleaned_action_id = teacher_action_id.strip()
    cleaned_title = title.strip()
    cleaned_teacher_note = teacher_note.strip()
    cleaned_practice_note = practice_note.strip()
    if not cleaned_action_id or not cleaned_title or not cleaned_teacher_note or not cleaned_practice_note:
        raise ValueError("missing required intervention assignment field")

    _ensure_tables(store.db_path)
    now = _now_ts()
    with _connect(store.db_path) as conn:
        action = conn.execute(
            """
            SELECT id, target_type, target_id, topic
            FROM teacher_actions
            WHERE id = ?
            """,
            (cleaned_action_id,),
        ).fetchone()
        if action is None:
            raise KeyError(cleaned_action_id)

        record = {
            "id": f"intervention-assignment:{uuid4().hex}",
            "teacher_action_id": cleaned_action_id,
            "target_type": action["target_type"],
            "target_id": action["target_id"],
            "assignment_type": assignment_type,
            "topic": action["topic"],
            "title": cleaned_title,
            "teacher_note": cleaned_teacher_note,
            "practice_note": cleaned_practice_note,
            "status": "planned",
            "created_at": now,
            "updated_at": now,
        }
        conn.execute(
            """
            INSERT INTO intervention_assignments (
                id, teacher_action_id, target_type, target_id, assignment_type,
                topic, title, teacher_note, practice_note, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["teacher_action_id"],
                record["target_type"],
                record["target_id"],
                record["assignment_type"],
                record["topic"],
                record["title"],
                record["teacher_note"],
                record["practice_note"],
                record["status"],
                record["created_at"],
                record["updated_at"],
            ),
        )
        conn.commit()
    return deepcopy(record)


def update_intervention_assignment_status(
    store: Any,
    assignment_id: str,
    *,
    status: str,
) -> dict[str, Any]:
    if status not in _ALLOWED_ASSIGNMENT_STATUSES:
        raise ValueError("invalid status")

    _ensure_tables(store.db_path)
    now = _now_ts()
    with _connect(store.db_path) as conn:
        row = conn.execute(
            """
            SELECT id, teacher_action_id, target_type, target_id, assignment_type,
                   topic, title, teacher_note, practice_note, status, created_at, updated_at
            FROM intervention_assignments
            WHERE id = ?
            """,
            (assignment_id,),
        ).fetchone()
        if row is None:
            raise KeyError(assignment_id)

        conn.execute(
            """
            UPDATE intervention_assignments
            SET status = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, now, assignment_id),
        )
        conn.commit()

        updated = dict(_row_to_record(row))
        updated["status"] = status
        updated["updated_at"] = now
        return updated
