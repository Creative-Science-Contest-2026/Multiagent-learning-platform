"""
SQLite-backed unified chat session store.
"""

from __future__ import annotations

import asyncio
from collections import Counter
import json
import os
import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deeptutor.services.path_service import get_path_service


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _json_loads(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


@dataclass
class TurnRecord:
    id: str
    session_id: str
    capability: str
    status: str
    error: str
    created_at: float
    updated_at: float
    finished_at: float | None
    last_seq: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "turn_id": self.id,
            "session_id": self.session_id,
            "capability": self.capability,
            "status": self.status,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "finished_at": self.finished_at,
            "last_seq": self.last_seq,
        }


class SQLiteSessionStore:
    """Persist unified chat sessions and messages in a SQLite database."""

    def __init__(self, db_path: Path | None = None) -> None:
        path_service = get_path_service()
        self.db_path = db_path or path_service.get_chat_history_db()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._migrate_legacy_db(path_service)
        self._lock = asyncio.Lock()
        self._initialize()

    def _migrate_legacy_db(self, path_service) -> None:
        """Move the legacy ``data/chat_history.db`` into ``data/user/`` once."""
        legacy_path = path_service.project_root / "data" / "chat_history.db"
        if self.db_path.exists() or not legacy_path.exists() or legacy_path == self.db_path:
            return
        try:
            os.replace(legacy_path, self.db_path)
        except OSError:
            # Fall back to leaving the legacy DB in place if an OS-level move
            # is not possible; the new DB path will be initialized empty.
            pass

    def _initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'New conversation',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    compressed_summary TEXT DEFAULT '',
                    summary_up_to_msg_id INTEGER DEFAULT 0,
                    preferences_json TEXT DEFAULT '{}'
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    capability TEXT DEFAULT '',
                    events_json TEXT DEFAULT '',
                    attachments_json TEXT DEFAULT '',
                    created_at REAL NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session_created
                    ON messages(session_id, created_at, id);

                CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
                    ON sessions(updated_at DESC);

                CREATE TABLE IF NOT EXISTS turns (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                    capability TEXT DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'running',
                    error TEXT DEFAULT '',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    finished_at REAL
                );

                CREATE INDEX IF NOT EXISTS idx_turns_session_updated
                    ON turns(session_id, updated_at DESC);

                CREATE INDEX IF NOT EXISTS idx_turns_session_status
                    ON turns(session_id, status, updated_at DESC);

                CREATE TABLE IF NOT EXISTS turn_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turn_id TEXT NOT NULL REFERENCES turns(id) ON DELETE CASCADE,
                    seq INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    source TEXT DEFAULT '',
                    stage TEXT DEFAULT '',
                    content TEXT DEFAULT '',
                    metadata_json TEXT DEFAULT '',
                    timestamp REAL NOT NULL,
                    created_at REAL NOT NULL,
                    UNIQUE(turn_id, seq)
                );

                CREATE INDEX IF NOT EXISTS idx_turn_events_turn_seq
                    ON turn_events(turn_id, seq);

                CREATE TABLE IF NOT EXISTS observations (
                    observation_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    source TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    question_id TEXT DEFAULT '',
                    is_correct INTEGER NOT NULL,
                    latency_seconds INTEGER,
                    hint_count INTEGER NOT NULL DEFAULT 0,
                    retry_count INTEGER NOT NULL DEFAULT 0,
                    dominant_error TEXT DEFAULT '',
                    created_at REAL NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_observations_student_created
                    ON observations(student_id, created_at DESC);

                CREATE TABLE IF NOT EXISTS student_states (
                    student_id TEXT PRIMARY KEY,
                    repeated_mistakes_json TEXT NOT NULL DEFAULT '[]',
                    support_level TEXT NOT NULL DEFAULT 'independent',
                    confidence_trend TEXT NOT NULL DEFAULT 'flat',
                    recency_summary_json TEXT NOT NULL DEFAULT '{}',
                    mastery_signals_json TEXT NOT NULL DEFAULT '{}',
                    support_signals_json TEXT NOT NULL DEFAULT '{}',
                    misconception_signals_json TEXT NOT NULL DEFAULT '{}',
                    updated_at REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS class_rosters (
                    class_id TEXT PRIMARY KEY,
                    teacher_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_class_rosters_teacher_updated
                    ON class_rosters(teacher_id, updated_at DESC);

                CREATE TABLE IF NOT EXISTS class_roster_students (
                    class_id TEXT NOT NULL REFERENCES class_rosters(class_id) ON DELETE CASCADE,
                    student_id TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    PRIMARY KEY (class_id, student_id)
                );

                CREATE INDEX IF NOT EXISTS idx_class_roster_students_student
                    ON class_roster_students(student_id, class_id);
                """
            )
            columns = {row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()}
            if "preferences_json" not in columns:
                conn.execute(
                    "ALTER TABLE sessions ADD COLUMN preferences_json TEXT DEFAULT '{}'"
                )
            student_state_columns = {
                row[1] for row in conn.execute("PRAGMA table_info(student_states)").fetchall()
            }
            if "recency_summary_json" not in student_state_columns:
                conn.execute(
                    "ALTER TABLE student_states ADD COLUMN recency_summary_json TEXT NOT NULL DEFAULT '{}'"
                )
            if "mastery_signals_json" not in student_state_columns:
                conn.execute(
                    "ALTER TABLE student_states ADD COLUMN mastery_signals_json TEXT NOT NULL DEFAULT '{}'"
                )
            if "support_signals_json" not in student_state_columns:
                conn.execute(
                    "ALTER TABLE student_states ADD COLUMN support_signals_json TEXT NOT NULL DEFAULT '{}'"
                )
            if "misconception_signals_json" not in student_state_columns:
                conn.execute(
                    "ALTER TABLE student_states ADD COLUMN misconception_signals_json TEXT NOT NULL DEFAULT '{}'"
                )
            conn.commit()

    async def _run(self, fn, *args):
        async with self._lock:
            return await asyncio.to_thread(fn, *args)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_session_sync(self, title: str | None = None, session_id: str | None = None) -> dict[str, Any]:
        now = time.time()
        resolved_id = session_id or f"unified_{int(now * 1000)}_{uuid.uuid4().hex[:8]}"
        resolved_title = (title or "New conversation").strip() or "New conversation"
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sessions (id, title, created_at, updated_at, compressed_summary, summary_up_to_msg_id)
                VALUES (?, ?, ?, ?, '', 0)
                """,
                (resolved_id, resolved_title[:100], now, now),
            )
            conn.commit()
        return {
            "id": resolved_id,
            "session_id": resolved_id,
            "title": resolved_title[:100],
            "created_at": now,
            "updated_at": now,
            "compressed_summary": "",
            "summary_up_to_msg_id": 0,
        }

    async def create_session(self, title: str | None = None, session_id: str | None = None) -> dict[str, Any]:
        return await self._run(self._create_session_sync, title, session_id)

    def _get_session_sync(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    s.id,
                    s.title,
                    s.created_at,
                    s.updated_at,
                    s.compressed_summary,
                    s.summary_up_to_msg_id,
                    s.preferences_json,
                    COALESCE(
                        (
                            SELECT t.status
                            FROM turns t
                            WHERE t.session_id = s.id
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        'idle'
                    ) AS status,
                    COALESCE(
                        (
                            SELECT t.id
                            FROM turns t
                            WHERE t.session_id = s.id AND t.status = 'running'
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        ''
                    ) AS active_turn_id,
                    COALESCE(
                        (
                            SELECT t.capability
                            FROM turns t
                            WHERE t.session_id = s.id
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        ''
                    ) AS capability
                FROM sessions
                s
                WHERE s.id = ?
                """,
                (session_id,),
            ).fetchone()
        if not row:
            return None
        payload = dict(row)
        payload["session_id"] = payload["id"]
        payload["preferences"] = _json_loads(payload.pop("preferences_json", ""), {})
        return payload

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        return await self._run(self._get_session_sync, session_id)

    async def ensure_session(self, session_id: str | None = None) -> dict[str, Any]:
        if session_id:
            session = await self.get_session(session_id)
            if session is not None:
                return session
        return await self.create_session()

    @staticmethod
    def _serialize_turn(row: sqlite3.Row) -> dict[str, Any]:
        return TurnRecord(
            id=row["id"],
            session_id=row["session_id"],
            capability=row["capability"] or "",
            status=row["status"] or "running",
            error=row["error"] or "",
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            finished_at=row["finished_at"],
            last_seq=row["last_seq"] if "last_seq" in row.keys() else 0,
        ).to_dict()

    def _create_turn_sync(self, session_id: str, capability: str = "") -> dict[str, Any]:
        now = time.time()
        turn_id = f"turn_{int(now * 1000)}_{uuid.uuid4().hex[:10]}"
        with self._connect() as conn:
            session = conn.execute("SELECT id FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if session is None:
                raise ValueError(f"Session not found: {session_id}")
            active = conn.execute(
                """
                SELECT id
                FROM turns
                WHERE session_id = ? AND status = 'running'
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                (session_id,),
            ).fetchone()
            if active is not None:
                raise RuntimeError(f"Session already has an active turn: {active['id']}")
            conn.execute(
                """
                INSERT INTO turns (id, session_id, capability, status, error, created_at, updated_at, finished_at)
                VALUES (?, ?, ?, 'running', '', ?, ?, NULL)
                """,
                (turn_id, session_id, capability or "", now, now),
            )
            conn.commit()
        return {
            "id": turn_id,
            "turn_id": turn_id,
            "session_id": session_id,
            "capability": capability or "",
            "status": "running",
            "error": "",
            "created_at": now,
            "updated_at": now,
            "finished_at": None,
            "last_seq": 0,
        }

    async def create_turn(self, session_id: str, capability: str = "") -> dict[str, Any]:
        return await self._run(self._create_turn_sync, session_id, capability)

    def _get_turn_sync(self, turn_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    t.*,
                    COALESCE((SELECT MAX(seq) FROM turn_events te WHERE te.turn_id = t.id), 0) AS last_seq
                FROM turns t
                WHERE t.id = ?
                """,
                (turn_id,),
            ).fetchone()
        if row is None:
            return None
        return self._serialize_turn(row)

    async def get_turn(self, turn_id: str) -> dict[str, Any] | None:
        return await self._run(self._get_turn_sync, turn_id)

    def _get_active_turn_sync(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    t.*,
                    COALESCE((SELECT MAX(seq) FROM turn_events te WHERE te.turn_id = t.id), 0) AS last_seq
                FROM turns t
                WHERE t.session_id = ? AND t.status = 'running'
                ORDER BY t.updated_at DESC
                LIMIT 1
                """,
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        return self._serialize_turn(row)

    async def get_active_turn(self, session_id: str) -> dict[str, Any] | None:
        return await self._run(self._get_active_turn_sync, session_id)

    def _list_active_turns_sync(self, session_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    t.*,
                    COALESCE((SELECT MAX(seq) FROM turn_events te WHERE te.turn_id = t.id), 0) AS last_seq
                FROM turns t
                WHERE t.session_id = ? AND t.status = 'running'
                ORDER BY t.updated_at DESC
                """,
                (session_id,),
            ).fetchall()
        return [self._serialize_turn(row) for row in rows]

    async def list_active_turns(self, session_id: str) -> list[dict[str, Any]]:
        return await self._run(self._list_active_turns_sync, session_id)

    def _update_turn_status_sync(self, turn_id: str, status: str, error: str = "") -> bool:
        now = time.time()
        finished_at = now if status in {"completed", "failed", "cancelled"} else None
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE turns
                SET status = ?, error = ?, updated_at = ?, finished_at = ?
                WHERE id = ?
                """,
                (status, error or "", now, finished_at, turn_id),
            )
            conn.commit()
        return cur.rowcount > 0

    async def update_turn_status(self, turn_id: str, status: str, error: str = "") -> bool:
        return await self._run(self._update_turn_status_sync, turn_id, status, error)

    def _append_turn_event_sync(self, turn_id: str, event: dict[str, Any]) -> dict[str, Any]:
        now = time.time()
        with self._connect() as conn:
            turn = conn.execute("SELECT id, session_id FROM turns WHERE id = ?", (turn_id,)).fetchone()
            if turn is None:
                raise ValueError(f"Turn not found: {turn_id}")
            provided_seq = int(event.get("seq") or 0)
            if provided_seq > 0:
                seq = provided_seq
            else:
                row = conn.execute(
                    "SELECT COALESCE(MAX(seq), 0) AS last_seq FROM turn_events WHERE turn_id = ?",
                    (turn_id,),
                ).fetchone()
                seq = int(row["last_seq"]) + 1 if row else 1
            payload = dict(event)
            payload["seq"] = seq
            payload["turn_id"] = payload.get("turn_id") or turn_id
            payload["session_id"] = payload.get("session_id") or turn["session_id"]
            conn.execute(
                """
                INSERT OR REPLACE INTO turn_events (
                    turn_id, seq, type, source, stage, content, metadata_json, timestamp, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    turn_id,
                    seq,
                    payload.get("type", ""),
                    payload.get("source", ""),
                    payload.get("stage", ""),
                    payload.get("content", "") or "",
                    _json_dumps(payload.get("metadata", {})),
                    float(payload.get("timestamp") or now),
                    now,
                ),
            )
            conn.execute(
                "UPDATE turns SET updated_at = ? WHERE id = ?",
                (now, turn_id),
            )
            conn.commit()
        return payload

    async def append_turn_event(self, turn_id: str, event: dict[str, Any]) -> dict[str, Any]:
        return await self._run(self._append_turn_event_sync, turn_id, event)

    def _get_turn_events_sync(self, turn_id: str, after_seq: int = 0) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT turn_id, seq, type, source, stage, content, metadata_json, timestamp
                FROM turn_events
                WHERE turn_id = ? AND seq > ?
                ORDER BY seq ASC
                """,
                (turn_id, max(0, int(after_seq))),
            ).fetchall()
            turn = conn.execute("SELECT session_id FROM turns WHERE id = ?", (turn_id,)).fetchone()
        session_id = turn["session_id"] if turn else ""
        return [
            {
                "type": row["type"],
                "source": row["source"] or "",
                "stage": row["stage"] or "",
                "content": row["content"] or "",
                "metadata": _json_loads(row["metadata_json"], {}),
                "session_id": session_id,
                "turn_id": row["turn_id"],
                "seq": row["seq"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    async def get_turn_events(self, turn_id: str, after_seq: int = 0) -> list[dict[str, Any]]:
        return await self._run(self._get_turn_events_sync, turn_id, after_seq)

    def _save_observations_sync(self, observations: list[dict[str, Any]]) -> None:
        now = time.time()
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO observations (
                    observation_id, session_id, student_id, source, topic, question_id,
                    is_correct, latency_seconds, hint_count, retry_count, dominant_error, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        row["observation_id"],
                        row["session_id"],
                        row["student_id"],
                        row["source"],
                        row["topic"],
                        row["question_id"],
                        1 if row["is_correct"] else 0,
                        row["latency_seconds"],
                        row["hint_count"],
                        row["retry_count"],
                        row["dominant_error"] or "",
                        float(row.get("created_at") or now),
                    )
                    for row in observations
                ],
            )
            conn.commit()

    async def save_observations(self, observations: list[dict[str, Any]]) -> None:
        return await self._run(self._save_observations_sync, observations)

    def _upsert_student_state_sync(self, student_id: str, state: dict[str, Any]) -> None:
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO student_states (
                    student_id, repeated_mistakes_json, support_level, confidence_trend, recency_summary_json,
                    mastery_signals_json, support_signals_json, misconception_signals_json, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(student_id) DO UPDATE SET
                    repeated_mistakes_json = excluded.repeated_mistakes_json,
                    support_level = excluded.support_level,
                    confidence_trend = excluded.confidence_trend,
                    recency_summary_json = excluded.recency_summary_json,
                    mastery_signals_json = excluded.mastery_signals_json,
                    support_signals_json = excluded.support_signals_json,
                    misconception_signals_json = excluded.misconception_signals_json,
                    updated_at = excluded.updated_at
                """,
                (
                    student_id,
                    _json_dumps(state.get("repeated_mistakes", [])),
                    state.get("support_level", "independent"),
                    state.get("confidence_trend", "flat"),
                    _json_dumps(state.get("recency_summary", {})),
                    _json_dumps(state.get("mastery_signals", {})),
                    _json_dumps(state.get("support_signals", {})),
                    _json_dumps(state.get("misconception_signals", {})),
                    now,
                ),
            )
            conn.commit()

    async def upsert_student_state(self, student_id: str, state: dict[str, Any]) -> None:
        return await self._run(self._upsert_student_state_sync, student_id, state)

    def _create_class_roster_sync(
        self,
        class_id: str,
        teacher_id: str,
        title: str,
        student_ids: list[str],
    ) -> dict[str, Any]:
        cleaned_class_id = class_id.strip()
        cleaned_teacher_id = teacher_id.strip()
        cleaned_title = title.strip()
        cleaned_student_ids = [sid for sid in dict.fromkeys(s.strip() for s in student_ids) if sid]
        if not cleaned_class_id or not cleaned_teacher_id or not cleaned_title:
            raise ValueError("class_id, teacher_id, and title are required")
        if not cleaned_student_ids:
            raise ValueError("student_ids must not be empty")

        now = time.time()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO class_rosters (class_id, teacher_id, title, metadata_json, created_at, updated_at)
                VALUES (?, ?, ?, '{}', ?, ?)
                ON CONFLICT(class_id) DO UPDATE SET
                    teacher_id = excluded.teacher_id,
                    title = excluded.title,
                    updated_at = excluded.updated_at
                """,
                (cleaned_class_id, cleaned_teacher_id, cleaned_title, now, now),
            )
            conn.execute("DELETE FROM class_roster_students WHERE class_id = ?", (cleaned_class_id,))
            conn.executemany(
                """
                INSERT INTO class_roster_students (class_id, student_id, created_at)
                VALUES (?, ?, ?)
                """,
                [(cleaned_class_id, student_id, now) for student_id in cleaned_student_ids],
            )
            conn.commit()

        return {
            "class_id": cleaned_class_id,
            "teacher_id": cleaned_teacher_id,
            "title": cleaned_title,
            "student_ids": cleaned_student_ids,
            "created_at": now,
            "updated_at": now,
        }

    async def create_class_roster(
        self,
        *,
        class_id: str,
        teacher_id: str,
        title: str,
        student_ids: list[str],
    ) -> dict[str, Any]:
        return await self._run(
            self._create_class_roster_sync,
            class_id,
            teacher_id,
            title,
            student_ids,
        )

    def _get_class_roster_sync(self, class_id: str) -> dict[str, Any] | None:
        cleaned_class_id = class_id.strip()
        if not cleaned_class_id:
            return None
        with self._connect() as conn:
            roster = conn.execute(
                """
                SELECT class_id, teacher_id, title, created_at, updated_at
                FROM class_rosters
                WHERE class_id = ?
                """,
                (cleaned_class_id,),
            ).fetchone()
            if roster is None:
                return None
            members = conn.execute(
                """
                SELECT student_id
                FROM class_roster_students
                WHERE class_id = ?
                ORDER BY student_id
                """,
                (cleaned_class_id,),
            ).fetchall()
        return {
            "class_id": roster["class_id"],
            "teacher_id": roster["teacher_id"],
            "title": roster["title"],
            "student_ids": [row["student_id"] for row in members],
            "created_at": roster["created_at"],
            "updated_at": roster["updated_at"],
        }

    async def get_class_roster(self, class_id: str) -> dict[str, Any] | None:
        return await self._run(self._get_class_roster_sync, class_id)

    def _list_teacher_roster_student_ids_sync(
        self,
        teacher_id: str,
        class_id: str | None = None,
    ) -> list[str]:
        cleaned_teacher_id = teacher_id.strip()
        if not cleaned_teacher_id:
            return []
        query = """
            SELECT DISTINCT members.student_id
            FROM class_rosters rosters
            JOIN class_roster_students members ON members.class_id = rosters.class_id
            WHERE rosters.teacher_id = ?
        """
        params: list[Any] = [cleaned_teacher_id]
        if class_id and class_id.strip():
            query += " AND rosters.class_id = ?"
            params.append(class_id.strip())
        query += " ORDER BY members.student_id"
        with self._connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()
        return [str(row["student_id"]) for row in rows]

    async def list_teacher_roster_student_ids(
        self,
        teacher_id: str,
        *,
        class_id: str | None = None,
    ) -> list[str]:
        return await self._run(self._list_teacher_roster_student_ids_sync, teacher_id, class_id)

    def _get_student_state_sync(self, student_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT student_id, repeated_mistakes_json, support_level, confidence_trend, recency_summary_json,
                       mastery_signals_json, support_signals_json, misconception_signals_json, updated_at
                FROM student_states
                WHERE student_id = ?
                """,
                (student_id,),
            ).fetchone()
        if row is None:
            return None
        return {
            "student_id": row["student_id"],
            "repeated_mistakes": _json_loads(row["repeated_mistakes_json"], []),
            "support_level": row["support_level"],
            "confidence_trend": row["confidence_trend"],
            "recency_summary": _json_loads(row["recency_summary_json"], {}),
            "mastery_signals": _json_loads(row["mastery_signals_json"], {}),
            "support_signals": _json_loads(row["support_signals_json"], {}),
            "misconception_signals": _json_loads(row["misconception_signals_json"], {}),
            "updated_at": row["updated_at"],
        }

    async def get_student_state(self, student_id: str) -> dict[str, Any] | None:
        return await self._run(self._get_student_state_sync, student_id)

    def _list_observations_sync(self, student_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT observation_id, session_id, student_id, source, topic, question_id, is_correct,
                       latency_seconds, hint_count, retry_count, dominant_error, created_at
                FROM observations
                WHERE student_id = ?
                ORDER BY created_at DESC
                """,
                (student_id,),
            ).fetchall()
        return [
            {
                "observation_id": row["observation_id"],
                "session_id": row["session_id"],
                "student_id": row["student_id"],
                "source": row["source"],
                "topic": row["topic"],
                "question_id": row["question_id"],
                "is_correct": bool(row["is_correct"]),
                "latency_seconds": row["latency_seconds"],
                "hint_count": row["hint_count"],
                "retry_count": row["retry_count"],
                "dominant_error": row["dominant_error"] or None,
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    async def list_observations(self, student_id: str) -> list[dict[str, Any]]:
        return await self._run(self._list_observations_sync, student_id)

    @staticmethod
    def _recency_bucket(age_seconds: float) -> str:
        day = 24 * 60 * 60
        if age_seconds <= day:
            return "last_24h"
        if age_seconds <= 7 * day:
            return "last_7d"
        if age_seconds <= 30 * day:
            return "last_30d"
        return "older"

    def _build_student_state_rollup_sync(self, student_id: str, limit: int = 24) -> dict[str, Any] | None:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT topic, is_correct, hint_count, retry_count, dominant_error, created_at
                FROM observations
                WHERE student_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (student_id, max(1, int(limit))),
            ).fetchall()
        if not rows:
            return None

        now = time.time()
        weighted_topic_misses: Counter[str] = Counter()
        topic_attempts: Counter[str] = Counter()
        topic_correct: Counter[str] = Counter()
        heavy_hint_topics: Counter[str] = Counter()
        retry_heavy_topics: Counter[str] = Counter()
        dominant_errors: Counter[tuple[str, str]] = Counter()
        recent_rows = []
        recency_counter: Counter[str] = Counter()
        for row in rows:
            topic = str(row["topic"] or "general")
            is_correct = bool(row["is_correct"])
            hint_count = int(row["hint_count"] or 0)
            retry_count = int(row["retry_count"] or 0)
            dominant_error = str(row["dominant_error"] or "").strip()
            created_at = float(row["created_at"] or now)
            age_seconds = max(0.0, now - created_at)
            recency_counter[self._recency_bucket(age_seconds)] += 1
            topic_attempts[topic] += 1
            if is_correct:
                topic_correct[topic] += 1

            if not is_correct:
                half_life_seconds = 7 * 24 * 60 * 60
                weight = 2 ** (-age_seconds / half_life_seconds)
                weighted_topic_misses[topic] += weight
            if hint_count >= 2:
                heavy_hint_topics[topic] += 1
            if retry_count >= 2:
                retry_heavy_topics[topic] += 1
            if dominant_error:
                dominant_errors[(topic, dominant_error)] += 1
            recent_rows.append((topic, is_correct, hint_count, retry_count))

        repeated_mistakes = [
            topic
            for topic, _score in sorted(
                weighted_topic_misses.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:3]
        ]

        recent_slice = recent_rows[: min(8, len(recent_rows))]
        incorrect_recent = sum(1 for item in recent_slice if not item[1])
        heavy_support_recent = sum(1 for item in recent_slice if item[2] >= 2 or item[3] >= 2)
        if incorrect_recent >= 3 and heavy_support_recent >= 2:
            support_level = "intensive"
        elif incorrect_recent >= 1 or heavy_support_recent >= 1:
            support_level = "guided"
        else:
            support_level = "independent"

        chronological = list(reversed(recent_slice))
        perf_scores: list[float] = []
        for _topic, is_correct, hint_count, retry_count in chronological:
            base = 1.0 if is_correct else -1.0
            base -= 0.15 * min(3, hint_count)
            base -= 0.1 * min(3, retry_count)
            perf_scores.append(base)
        split = max(1, len(perf_scores) // 2)
        early_avg = sum(perf_scores[:split]) / split
        late_len = max(1, len(perf_scores) - split)
        late_avg = sum(perf_scores[split:]) / late_len
        delta = late_avg - early_avg
        if delta > 0.2:
            confidence_trend = "up"
        elif delta < -0.2:
            confidence_trend = "down"
        else:
            confidence_trend = "flat"

        recency_summary = {
            "total_observations": len(rows),
            "window_size": max(1, int(limit)),
            "bucket_counts": {
                "last_24h": recency_counter.get("last_24h", 0),
                "last_7d": recency_counter.get("last_7d", 0),
                "last_30d": recency_counter.get("last_30d", 0),
                "older": recency_counter.get("older", 0),
            },
            "recent_incorrect": incorrect_recent,
            "weighted_topic_misses": {
                topic: round(score, 3) for topic, score in weighted_topic_misses.items()
            },
        }

        at_risk_topics = [
            topic
            for topic, _score in sorted(weighted_topic_misses.items(), key=lambda item: item[1], reverse=True)
            if weighted_topic_misses[topic] >= 0.5
        ][:3]
        stable_topics = [
            topic
            for topic, attempts in topic_attempts.items()
            if attempts >= 2 and topic_correct[topic] == attempts
        ][:3]
        emerging_topics = [
            topic
            for topic in repeated_mistakes
            if topic not in at_risk_topics
        ][:3]

        if heavy_support_recent >= 3:
            recent_support_burden = "high"
        elif heavy_support_recent >= 1:
            recent_support_burden = "elevated"
        else:
            recent_support_burden = "steady"

        dominant_error_by_topic: dict[str, str] = {}
        for (topic, error), _count in dominant_errors.most_common():
            dominant_error_by_topic.setdefault(topic, error)
        persistent_topics = [
            topic
            for topic in repeated_mistakes
            if topic in dominant_error_by_topic or topic in at_risk_topics
        ]

        return {
            "student_id": student_id,
            "repeated_mistakes": repeated_mistakes,
            "support_level": support_level,
            "confidence_trend": confidence_trend,
            "recency_summary": recency_summary,
            "mastery_signals": {
                "emerging_topics": emerging_topics,
                "stable_topics": stable_topics,
                "at_risk_topics": at_risk_topics,
            },
            "support_signals": {
                "heavy_hint_topics": list(heavy_hint_topics.keys())[:3],
                "retry_heavy_topics": list(retry_heavy_topics.keys())[:3],
                "recent_support_burden": recent_support_burden,
            },
            "misconception_signals": {
                "dominant_errors": dominant_error_by_topic,
                "persistent_topics": persistent_topics[:3],
            },
        }

    async def build_student_state_rollup(self, student_id: str, limit: int = 24) -> dict[str, Any] | None:
        return await self._run(self._build_student_state_rollup_sync, student_id, limit)

    def _update_session_title_sync(self, session_id: str, title: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE sessions
                SET title = ?, updated_at = ?
                WHERE id = ?
                """,
                ((title.strip() or "New conversation")[:100], time.time(), session_id),
            )
            conn.commit()
        return cur.rowcount > 0

    async def update_session_title(self, session_id: str, title: str) -> bool:
        return await self._run(self._update_session_title_sync, session_id, title)

    def _delete_session_sync(self, session_id: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
        return cur.rowcount > 0

    async def delete_session(self, session_id: str) -> bool:
        return await self._run(self._delete_session_sync, session_id)

    def _add_message_sync(
        self,
        session_id: str,
        role: str,
        content: str,
        capability: str = "",
        events: list[dict[str, Any]] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> int:
        now = time.time()
        with self._connect() as conn:
            session = conn.execute("SELECT id, title FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if session is None:
                raise ValueError(f"Session not found: {session_id}")

            cur = conn.execute(
                """
                INSERT INTO messages (
                    session_id, role, content, capability, events_json, attachments_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    role,
                    content or "",
                    capability or "",
                    _json_dumps(events or []),
                    _json_dumps(attachments or []),
                    now,
                ),
            )

            title = None
            if session["title"] == "New conversation" and role == "user":
                trimmed = (content or "").strip()
                if trimmed:
                    title = trimmed[:50] + ("..." if len(trimmed) > 50 else "")

            conn.execute(
                "UPDATE sessions SET updated_at = ? WHERE id = ?",
                (now, session_id),
            )
            if title:
                conn.execute(
                    "UPDATE sessions SET title = ? WHERE id = ?",
                    (title, session_id),
                )
            conn.commit()
            return int(cur.lastrowid)

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        capability: str = "",
        events: list[dict[str, Any]] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> int:
        return await self._run(
            self._add_message_sync,
            session_id,
            role,
            content,
            capability,
            events,
            attachments,
        )

    def _serialize_message(self, row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "session_id": row["session_id"],
            "role": row["role"],
            "content": row["content"],
            "capability": row["capability"] or "",
            "events": _json_loads(row["events_json"], []),
            "attachments": _json_loads(row["attachments_json"], []),
            "created_at": row["created_at"],
        }

    def _get_messages_sync(self, session_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, session_id, role, content, capability, events_json, attachments_json, created_at
                FROM messages
                WHERE session_id = ?
                ORDER BY id ASC
                """,
                (session_id,),
            ).fetchall()
        return [self._serialize_message(row) for row in rows]

    async def get_messages(self, session_id: str) -> list[dict[str, Any]]:
        return await self._run(self._get_messages_sync, session_id)

    def _get_messages_for_context_sync(self, session_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, role, content
                FROM messages
                WHERE session_id = ?
                  AND role IN ('user', 'assistant', 'system')
                ORDER BY id ASC
                """,
                (session_id,),
            ).fetchall()
        return [
            {"id": row["id"], "role": row["role"], "content": row["content"] or ""}
            for row in rows
        ]

    async def get_messages_for_context(self, session_id: str) -> list[dict[str, Any]]:
        return await self._run(self._get_messages_for_context_sync, session_id)

    def _list_sessions_sync(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    s.id,
                    s.title,
                    s.created_at,
                    s.updated_at,
                    s.compressed_summary,
                    s.summary_up_to_msg_id,
                    s.preferences_json,
                    COUNT(m.id) AS message_count,
                    COALESCE(
                        (
                            SELECT t.status
                            FROM turns t
                            WHERE t.session_id = s.id
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        'idle'
                    ) AS status,
                    COALESCE(
                        (
                            SELECT t.id
                            FROM turns t
                            WHERE t.session_id = s.id AND t.status = 'running'
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        ''
                    ) AS active_turn_id,
                    COALESCE(
                        (
                            SELECT t.capability
                            FROM turns t
                            WHERE t.session_id = s.id
                            ORDER BY t.updated_at DESC
                            LIMIT 1
                        ),
                        ''
                    ) AS capability,
                    COALESCE(
                        (
                            SELECT m2.content
                            FROM messages m2
                            WHERE m2.session_id = s.id
                              AND TRIM(COALESCE(m2.content, '')) != ''
                            ORDER BY m2.id DESC
                            LIMIT 1
                        ),
                        ''
                    ) AS last_message
                FROM sessions s
                LEFT JOIN messages m ON m.session_id = s.id
                GROUP BY s.id
                ORDER BY s.updated_at DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
        sessions = []
        for row in rows:
            payload = dict(row)
            payload["session_id"] = payload["id"]
            payload["preferences"] = _json_loads(payload.pop("preferences_json", ""), {})
            sessions.append(payload)
        return sessions

    async def list_sessions(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        return await self._run(self._list_sessions_sync, limit, offset)

    def _update_summary_sync(self, session_id: str, summary: str, up_to_msg_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                """
                UPDATE sessions
                SET compressed_summary = ?, summary_up_to_msg_id = ?, updated_at = updated_at
                WHERE id = ?
                """,
                (summary, max(0, int(up_to_msg_id)), session_id),
            )
            conn.commit()
        return cur.rowcount > 0

    async def update_summary(self, session_id: str, summary: str, up_to_msg_id: int) -> bool:
        return await self._run(self._update_summary_sync, session_id, summary, up_to_msg_id)

    def _update_session_preferences_sync(self, session_id: str, preferences: dict[str, Any]) -> bool:
        with self._connect() as conn:
            current = conn.execute(
                "SELECT preferences_json FROM sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
            if current is None:
                return False
            merged = {
                **_json_loads(current["preferences_json"], {}),
                **(preferences or {}),
            }
            cur = conn.execute(
                """
                UPDATE sessions
                SET preferences_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (_json_dumps(merged), time.time(), session_id),
            )
            conn.commit()
        return cur.rowcount > 0

    async def update_session_preferences(self, session_id: str, preferences: dict[str, Any]) -> bool:
        return await self._run(self._update_session_preferences_sync, session_id, preferences)

    async def get_session_with_messages(self, session_id: str) -> dict[str, Any] | None:
        session = await self.get_session(session_id)
        if session is None:
            return None
        session["messages"] = await self.get_messages(session_id)
        session["active_turns"] = await self.list_active_turns(session_id)
        return session


_instance: SQLiteSessionStore | None = None


def get_sqlite_session_store() -> SQLiteSessionStore:
    global _instance
    if _instance is None:
        _instance = SQLiteSessionStore()
    return _instance


__all__ = ["SQLiteSessionStore", "get_sqlite_session_store"]
