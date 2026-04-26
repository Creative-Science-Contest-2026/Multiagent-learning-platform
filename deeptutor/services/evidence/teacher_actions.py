from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3
from typing import Any
from uuid import uuid4

_ALLOWED_ACTION_TYPES = {
    "reteach_concept",
    "scaffolded_practice",
    "review_prerequisite",
    "small_group_remediation",
}
_ALLOWED_PRIORITIES = {"low", "medium", "high"}
_ALLOWED_STATUSES = {"draft", "planned", "done", "dismissed"}


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
            CREATE TABLE IF NOT EXISTS teacher_actions (
                id TEXT PRIMARY KEY,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                source_recommendation_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                teacher_instruction TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_teacher_actions_target
                ON teacher_actions(target_type, target_id, updated_at DESC)
            """
        )
        conn.commit()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "target_type": row["target_type"],
        "target_id": row["target_id"],
        "source_recommendation_id": row["source_recommendation_id"],
        "action_type": row["action_type"],
        "topic": row["topic"],
        "teacher_instruction": row["teacher_instruction"],
        "priority": row["priority"],
        "status": row["status"],
        "created_at": int(row["created_at"]),
        "updated_at": int(row["updated_at"]),
    }


def list_teacher_actions(store: Any) -> list[dict[str, Any]]:
    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, target_type, target_id, source_recommendation_id, action_type,
                   topic, teacher_instruction, priority, status, created_at, updated_at
            FROM teacher_actions
            ORDER BY updated_at DESC, created_at DESC, id DESC
            """
        ).fetchall()
    return [_row_to_record(row) for row in rows]


def create_teacher_action(
    store: Any,
    *,
    target_type: str,
    target_id: str,
    source_recommendation_id: str,
    action_type: str,
    topic: str,
    teacher_instruction: str,
    priority: str,
) -> dict[str, Any]:
    if target_type not in {"student", "small_group"}:
        raise ValueError("invalid target_type")
    if action_type not in _ALLOWED_ACTION_TYPES:
        raise ValueError("invalid action_type")
    if priority not in _ALLOWED_PRIORITIES:
        raise ValueError("invalid priority")

    cleaned_target_id = target_id.strip()
    cleaned_source = source_recommendation_id.strip()
    cleaned_topic = topic.strip()
    cleaned_instruction = teacher_instruction.strip()
    if not cleaned_target_id or not cleaned_source or not cleaned_topic or not cleaned_instruction:
        raise ValueError("missing required teacher action field")

    now = _now_ts()
    record = {
        "id": f"teacher-action:{uuid4().hex}",
        "target_type": target_type,
        "target_id": cleaned_target_id,
        "source_recommendation_id": cleaned_source,
        "action_type": action_type,
        "topic": cleaned_topic,
        "teacher_instruction": cleaned_instruction,
        "priority": priority,
        "status": "planned",
        "created_at": now,
        "updated_at": now,
    }

    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        conn.execute(
            """
            INSERT INTO teacher_actions (
                id, target_type, target_id, source_recommendation_id, action_type,
                topic, teacher_instruction, priority, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["target_type"],
                record["target_id"],
                record["source_recommendation_id"],
                record["action_type"],
                record["topic"],
                record["teacher_instruction"],
                record["priority"],
                record["status"],
                record["created_at"],
                record["updated_at"],
            ),
        )
        conn.commit()
    return deepcopy(record)


def update_teacher_action_status(store: Any, action_id: str, *, status: str) -> dict[str, Any]:
    if status not in _ALLOWED_STATUSES:
        raise ValueError("invalid status")

    _ensure_table(store.db_path)
    now = _now_ts()
    with _connect(store.db_path) as conn:
        row = conn.execute(
            """
            SELECT id, target_type, target_id, source_recommendation_id, action_type,
                   topic, teacher_instruction, priority, status, created_at, updated_at
            FROM teacher_actions
            WHERE id = ?
            """,
            (action_id,),
        ).fetchone()
        if row is None:
            raise KeyError(action_id)

        conn.execute(
            """
            UPDATE teacher_actions
            SET status = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, now, action_id),
        )
        conn.commit()

        updated = dict(_row_to_record(row))
        updated["status"] = status
        updated["updated_at"] = now
        return updated
