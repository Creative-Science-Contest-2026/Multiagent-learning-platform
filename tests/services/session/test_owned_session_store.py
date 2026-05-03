from __future__ import annotations

import pytest

from deeptutor.services.session.sqlite_store import SQLiteSessionStore


@pytest.mark.asyncio
async def test_list_sessions_returns_only_rows_for_owner(tmp_path) -> None:
    store = SQLiteSessionStore(tmp_path / "owned-chat-history.db")
    teacher = "user_teacher"
    student = "user_student"

    await store.create_session(owner_user_id=teacher, title="Teacher chat")
    await store.create_session(owner_user_id=student, title="Student chat")

    sessions = await store.list_sessions(owner_user_id=teacher)

    assert [session["title"] for session in sessions] == ["Teacher chat"]
