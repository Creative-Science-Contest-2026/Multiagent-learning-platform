from __future__ import annotations

import argparse
import json
import sqlite3
import time
from pathlib import Path
from urllib.parse import urlparse

from deeptutor.services.session.sqlite_store import SQLiteSessionStore


DEMO_KB_ID = "contest-demo-quadratics"
ASSESSMENT_SESSION_ID = "contest-assessment-demo"
TUTOR_SESSION_ID = "contest-tutor-demo"

DEMO_METADATA = {
    "subject": "Mathematics",
    "grade": "Grade 9",
    "curriculum": "Vietnam secondary algebra",
    "learning_objectives": [
        "Solve quadratic equations",
        "Explain common mistakes",
    ],
    "owner": "Contest Demo Teacher",
    "sharing_status": "demo",
}


def _validate_local_api_base(api_base: str) -> None:
    parsed = urlparse(api_base)
    if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1"}:
        raise ValueError("Use a local API base such as http://localhost:8001")


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _seed_knowledge_pack(project_root: Path) -> Path:
    kb_root = project_root / "data" / "knowledge_bases"
    kb_dir = kb_root / DEMO_KB_ID
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)
    (kb_dir / "raw").mkdir(parents=True, exist_ok=True)

    metadata = {
        "name": DEMO_KB_ID,
        "description": "Contest demo Knowledge Pack for quadratic equations.",
        "rag_provider": "llamaindex",
        "status": "ready",
        **DEMO_METADATA,
    }
    _write_json(kb_dir / "metadata.json", metadata)

    config_path = kb_root / "kb_config.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            config = {}
    else:
        config = {}
    config.setdefault("knowledge_bases", {})
    config["knowledge_bases"][DEMO_KB_ID] = {
        "path": DEMO_KB_ID,
        "description": metadata["description"],
        "rag_provider": "llamaindex",
        "status": "ready",
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        **DEMO_METADATA,
    }
    _write_json(config_path, config)
    return kb_dir


def _insert_session(
    conn: sqlite3.Connection,
    *,
    session_id: str,
    title: str,
    capability: str,
    user_message: str,
    assistant_message: str,
) -> None:
    now = time.time()
    preferences = {
        "capability": capability,
        "tools": ["rag"],
        "knowledge_bases": [DEMO_KB_ID],
        "language": "en",
        "demo": True,
    }
    turn_id = f"turn-{session_id}"

    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.execute(
        """
        INSERT INTO sessions (
            id, title, created_at, updated_at, compressed_summary, summary_up_to_msg_id, preferences_json
        ) VALUES (?, ?, ?, ?, '', 0, ?)
        """,
        (session_id, title, now, now, json.dumps(preferences, ensure_ascii=False)),
    )
    conn.execute(
        """
        INSERT INTO messages (
            session_id, role, content, capability, events_json, attachments_json, created_at
        ) VALUES (?, 'user', ?, ?, '[]', '[]', ?)
        """,
        (session_id, user_message, capability, now),
    )
    conn.execute(
        """
        INSERT INTO messages (
            session_id, role, content, capability, events_json, attachments_json, created_at
        ) VALUES (?, 'assistant', ?, ?, '[]', '[]', ?)
        """,
        (session_id, assistant_message, capability, now + 1),
    )
    conn.execute(
        """
        INSERT INTO turns (id, session_id, capability, status, error, created_at, updated_at, finished_at)
        VALUES (?, ?, ?, 'completed', '', ?, ?, ?)
        """,
        (turn_id, session_id, capability, now, now + 1, now + 1),
    )


def _seed_sessions(project_root: Path) -> Path:
    db_path = project_root / "data" / "user" / "chat_history.db"
    SQLiteSessionStore(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        _insert_session(
            conn,
            session_id=ASSESSMENT_SESSION_ID,
            title="Contest Demo Assessment",
            capability="deep_question",
            user_message="Generate Grade 9 quadratic equation questions from contest-demo-quadratics.",
            assistant_message=(
                "Generated demo-safe questions with answers, explanations, and common mistakes "
                "for solving quadratic equations."
            ),
        )
        _insert_session(
            conn,
            session_id=TUTOR_SESSION_ID,
            title="Contest Demo Tutor",
            capability="chat",
            user_message="Help a student understand a common quadratic equation mistake.",
            assistant_message=(
                "The Tutor Agent explains how to check factoring steps and compare both roots "
                "against the original equation."
            ),
        )
        conn.commit()
    return db_path


def reset_demo_data(project_root: str | Path = ".", *, api_base: str = "http://localhost:8001") -> dict:
    _validate_local_api_base(api_base)
    root = Path(project_root).expanduser().resolve()
    kb_dir = _seed_knowledge_pack(root)
    db_path = _seed_sessions(root)
    return {
        "knowledge_pack": DEMO_KB_ID,
        "sessions": [ASSESSMENT_SESSION_ID, TUTOR_SESSION_ID],
        "paths": {
            "knowledge_pack": str(kb_dir),
            "session_db": str(db_path),
        },
        "api_base": api_base,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reset local contest demo-safe data.")
    parser.add_argument("--project-root", default=".", help="Repository root to write demo data under.")
    parser.add_argument("--api-base", default="http://localhost:8001", help="Local API base safety check.")
    args = parser.parse_args()
    result = reset_demo_data(args.project_root, api_base=args.api_base)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
