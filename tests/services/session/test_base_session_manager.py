from __future__ import annotations

from deeptutor.services.session.base_session_manager import BaseSessionManager


class _TestSessionManager(BaseSessionManager):
    MAX_SESSIONS = 2

    def __init__(self, sessions_file):
        self.module_name = "test-base-session-manager"
        self.path_service = None
        self.sessions_file = sessions_file
        self._ensure_file()

    def _get_session_id_prefix(self) -> str:
        return "test_"

    def _get_default_title(self) -> str:
        return "New test session"

    def _create_session_data(self, **kwargs):
        return {"kind": kwargs.get("kind", "test")}

    def _get_session_summary(self, session):
        return {
            "session_id": session["session_id"],
            "title": session["title"],
            "owner_user_id": session.get("owner_user_id", ""),
        }


def test_create_session_trims_only_current_owner(tmp_path) -> None:
    manager = _TestSessionManager(tmp_path / "sessions.json")

    session_a1 = manager.create_session(title="A1", owner_user_id="teacher-a")
    session_b1 = manager.create_session(title="B1", owner_user_id="teacher-b")
    session_a2 = manager.create_session(title="A2", owner_user_id="teacher-a")
    session_a3 = manager.create_session(title="A3", owner_user_id="teacher-a")

    teacher_a_sessions = manager.list_sessions(limit=10, include_messages=True, owner_user_id="teacher-a")
    teacher_b_sessions = manager.list_sessions(limit=10, include_messages=True, owner_user_id="teacher-b")

    assert [session["session_id"] for session in teacher_a_sessions] == [
        session_a3["session_id"],
        session_a2["session_id"],
    ]
    assert [session["session_id"] for session in teacher_b_sessions] == [session_b1["session_id"]]
    assert manager.get_session(session_a1["session_id"], owner_user_id="teacher-a") is None
