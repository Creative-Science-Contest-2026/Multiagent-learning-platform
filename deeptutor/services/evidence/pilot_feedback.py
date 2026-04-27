from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import sqlite3
from typing import Any
from uuid import uuid4

_ALLOWED_LEVELS = {"walkthrough", "limited_external_feedback", "pilot"}


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
            CREATE TABLE IF NOT EXISTS pilot_feedback (
                id TEXT PRIMARY KEY,
                evidence_level TEXT NOT NULL,
                source_label TEXT NOT NULL,
                participant_role TEXT NOT NULL,
                feedback_date TEXT NOT NULL,
                scope_note TEXT NOT NULL,
                finding_summary TEXT NOT NULL,
                recommendation_note TEXT NOT NULL,
                artifact_ref TEXT NOT NULL,
                verified_by TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pilot_feedback_date
                ON pilot_feedback(feedback_date DESC, updated_at DESC)
            """
        )
        conn.commit()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "evidence_level": row["evidence_level"],
        "source_label": row["source_label"],
        "participant_role": row["participant_role"],
        "feedback_date": row["feedback_date"],
        "scope_note": row["scope_note"],
        "finding_summary": row["finding_summary"],
        "recommendation_note": row["recommendation_note"],
        "artifact_ref": row["artifact_ref"],
        "verified_by": row["verified_by"],
        "created_at": int(row["created_at"]),
        "updated_at": int(row["updated_at"]),
    }


def list_pilot_feedback(store: Any) -> list[dict[str, Any]]:
    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, evidence_level, source_label, participant_role, feedback_date,
                   scope_note, finding_summary, recommendation_note, artifact_ref,
                   verified_by, created_at, updated_at
            FROM pilot_feedback
            ORDER BY feedback_date DESC, updated_at DESC, created_at DESC, id DESC
            """
        ).fetchall()
    return [_row_to_record(row) for row in rows]


def create_pilot_feedback(
    store: Any,
    *,
    evidence_level: str,
    source_label: str,
    participant_role: str = "",
    feedback_date: str,
    scope_note: str,
    finding_summary: str,
    recommendation_note: str = "",
    artifact_ref: str = "",
    verified_by: str = "",
) -> dict[str, Any]:
    if evidence_level not in _ALLOWED_LEVELS:
        raise ValueError("invalid evidence_level")

    cleaned_source = source_label.strip()
    cleaned_role = participant_role.strip()
    cleaned_date = feedback_date.strip()
    cleaned_scope = scope_note.strip()
    cleaned_finding = finding_summary.strip()
    cleaned_recommendation = recommendation_note.strip()
    cleaned_artifact = artifact_ref.strip()
    cleaned_verified = verified_by.strip()

    if not cleaned_source or not cleaned_date or not cleaned_scope or not cleaned_finding:
        raise ValueError("missing required pilot feedback field")

    now = _now_ts()
    record = {
        "id": f"pilot-feedback:{uuid4().hex}",
        "evidence_level": evidence_level,
        "source_label": cleaned_source,
        "participant_role": cleaned_role,
        "feedback_date": cleaned_date,
        "scope_note": cleaned_scope,
        "finding_summary": cleaned_finding,
        "recommendation_note": cleaned_recommendation,
        "artifact_ref": cleaned_artifact,
        "verified_by": cleaned_verified,
        "created_at": now,
        "updated_at": now,
    }

    _ensure_table(store.db_path)
    with _connect(store.db_path) as conn:
        conn.execute(
            """
            INSERT INTO pilot_feedback (
                id, evidence_level, source_label, participant_role, feedback_date,
                scope_note, finding_summary, recommendation_note, artifact_ref,
                verified_by, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record["evidence_level"],
                record["source_label"],
                record["participant_role"],
                record["feedback_date"],
                record["scope_note"],
                record["finding_summary"],
                record["recommendation_note"],
                record["artifact_ref"],
                record["verified_by"],
                record["created_at"],
                record["updated_at"],
            ),
        )
        conn.commit()
    return deepcopy(record)


def build_pilot_feedback_status(store: Any) -> dict[str, Any]:
    items = list_pilot_feedback(store)
    if not items:
        return {
            "status": "no_pilot_evidence_yet",
            "record_count": 0,
            "levels_present": [],
            "latest_feedback_date": None,
            "items": [],
        }

    levels_present = sorted({item["evidence_level"] for item in items})
    latest_feedback_date = max(item["feedback_date"] for item in items)
    return {
        "status": "feedback_records_available",
        "record_count": len(items),
        "levels_present": levels_present,
        "latest_feedback_date": latest_feedback_date,
        "items": items,
    }

