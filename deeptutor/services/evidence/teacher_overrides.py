from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3
from typing import Any
from uuid import uuid4

_ALLOWED_REASONS = {"different_strategy", "needs_more_context", "not_classroom_fit"}
_ALLOWED_MOVES = {
    "reteach_concept",
    "scaffolded_practice",
    "review_prerequisite",
    "small_group_remediation",
}


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
            CREATE TABLE IF NOT EXISTS teacher_overrides (
                id TEXT PRIMARY KEY,
                owner_user_id TEXT NOT NULL DEFAULT '',
                source_recommendation_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                override_reason TEXT NOT NULL,
                teacher_selected_move TEXT NOT NULL,
                teacher_note TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_teacher_overrides_target
                ON teacher_overrides(target_type, target_id, updated_at DESC)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_teacher_overrides_source
                ON teacher_overrides(source_recommendation_id, updated_at DESC)
            """
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(teacher_overrides)").fetchall()}
        if "owner_user_id" not in columns:
            conn.execute(
                "ALTER TABLE teacher_overrides ADD COLUMN owner_user_id TEXT NOT NULL DEFAULT ''"
            )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_teacher_overrides_owner
                ON teacher_overrides(owner_user_id, updated_at DESC)
            """
        )
        conn.commit()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "owner_user_id": row["owner_user_id"],
        "source_recommendation_id": row["source_recommendation_id"],
        "target_type": row["target_type"],
        "target_id": row["target_id"],
        "override_reason": row["override_reason"],
        "teacher_selected_move": row["teacher_selected_move"],
        "teacher_note": row["teacher_note"],
        "created_at": int(row["created_at"]),
        "updated_at": int(row["updated_at"]),
    }


def list_teacher_overrides(store: Any, *, owner_user_id: str | None = None) -> list[dict[str, Any]]:
    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        query = """
            SELECT id, source_recommendation_id, target_type, target_id, override_reason,
                   teacher_selected_move, teacher_note, created_at, updated_at, owner_user_id
            FROM teacher_overrides
            """
        params: list[str] = []
        if owner_user_id is not None:
            query += " WHERE owner_user_id = ?"
            params.append((owner_user_id or "").strip())
        query += " ORDER BY updated_at DESC, created_at DESC, id DESC"
        rows = conn.execute(query, params).fetchall()
    return [_row_to_record(row) for row in rows]


def create_teacher_override(
    store: Any,
    *,
    source_recommendation_id: str,
    target_type: str,
    target_id: str,
    override_reason: str,
    teacher_selected_move: str,
    teacher_note: str = "",
    owner_user_id: str = "",
) -> dict[str, Any]:
    if target_type not in {"student", "small_group"}:
        raise ValueError("invalid target_type")
    if override_reason not in _ALLOWED_REASONS:
        raise ValueError("invalid override_reason")
    if teacher_selected_move not in _ALLOWED_MOVES:
        raise ValueError("invalid teacher_selected_move")

    cleaned_source = source_recommendation_id.strip()
    cleaned_target_id = target_id.strip()
    cleaned_note = teacher_note.strip()
    if not cleaned_source or not cleaned_target_id:
        raise ValueError("missing required teacher override field")

    now = _now_ts()
    record = {
        "id": f"teacher-override:{uuid4().hex}",
        "owner_user_id": owner_user_id.strip(),
        "source_recommendation_id": cleaned_source,
        "target_type": target_type,
        "target_id": cleaned_target_id,
        "override_reason": override_reason,
        "teacher_selected_move": teacher_selected_move,
        "teacher_note": cleaned_note,
        "created_at": now,
        "updated_at": now,
    }

    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        conn.execute(
            """
            INSERT INTO teacher_overrides (
                id, owner_user_id, source_recommendation_id, target_type, target_id, override_reason,
                teacher_selected_move, teacher_note, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["owner_user_id"],
                record["source_recommendation_id"],
                record["target_type"],
                record["target_id"],
                record["override_reason"],
                record["teacher_selected_move"],
                record["teacher_note"],
                record["created_at"],
                record["updated_at"],
            ),
        )
        conn.commit()
    return deepcopy(record)


def update_teacher_override(
    store: Any,
    override_id: str,
    *,
    override_reason: str,
    teacher_selected_move: str,
    teacher_note: str | None = None,
    owner_user_id: str | None = None,
) -> dict[str, Any]:
    if override_reason not in _ALLOWED_REASONS:
        raise ValueError("invalid override_reason")
    if teacher_selected_move not in _ALLOWED_MOVES:
        raise ValueError("invalid teacher_selected_move")

    cleaned_note = teacher_note.strip() if teacher_note is not None else None
    _ensure_table(store.db_path)
    now = _now_ts()
    with _connect(store.db_path) as conn:
        query = """
            SELECT id, source_recommendation_id, target_type, target_id, override_reason,
                   teacher_selected_move, teacher_note, created_at, updated_at, owner_user_id
            FROM teacher_overrides
            WHERE id = ?
            """
        params: list[str] = [override_id]
        if owner_user_id is not None:
            query += " AND owner_user_id = ?"
            params.append((owner_user_id or "").strip())
        row = conn.execute(query, params).fetchone()
        if row is None:
            raise KeyError(override_id)

        next_note = cleaned_note if cleaned_note is not None else row["teacher_note"]
        conn.execute(
            """
            UPDATE teacher_overrides
            SET override_reason = ?, teacher_selected_move = ?, teacher_note = ?, updated_at = ?
            WHERE id = ?
            """,
            (override_reason, teacher_selected_move, next_note, now, override_id),
        )
        conn.commit()

        updated = dict(_row_to_record(row))
        updated["override_reason"] = override_reason
        updated["teacher_selected_move"] = teacher_selected_move
        updated["teacher_note"] = next_note
        updated["updated_at"] = now
        return updated
