from __future__ import annotations

import importlib

import pytest

pytest.importorskip("fastapi")

from deeptutor.services.auth.schemas import AuthenticatedUser

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
memory_module = importlib.import_module("deeptutor.api.routers.memory")
router = memory_module.router


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1/memory")
    return app


def _teacher_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        id="teacher-1",
        email="teacher@example.com",
        display_name="Teacher One",
        role="teacher",
    )


def _make_snapshot(
    summary: str = "",
    profile: str = "",
    summary_updated_at: str | None = None,
    profile_updated_at: str | None = None,
):
    return type(
        "Snapshot",
        (),
        {
            "summary": summary,
            "profile": profile,
            "summary_updated_at": summary_updated_at,
            "profile_updated_at": profile_updated_at,
        },
    )()


def test_memory_router_returns_single_document(monkeypatch) -> None:
    class FakeMemoryService:
        def read_snapshot(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return _make_snapshot(
                profile="## Preferences\n- Prefer concise answers.",
                profile_updated_at="2026-03-13T12:00:00+08:00",
            )

    monkeypatch.setattr("deeptutor.api.routers.memory.get_memory_service", lambda: FakeMemoryService())

    app = _build_app()
    app.dependency_overrides[memory_module.get_current_user] = _teacher_user
    with TestClient(app) as client:
        response = client.get("/api/v1/memory")

    assert response.status_code == 200
    body = response.json()
    assert body["profile"] == "## Preferences\n- Prefer concise answers."
    assert body["profile_updated_at"] == "2026-03-13T12:00:00+08:00"
    assert body["summary"] == ""
    assert body["summary_updated_at"] is None


def test_memory_router_requires_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.get("/api/v1/memory")

    assert response.status_code == 401


def test_memory_router_refreshes_from_session(monkeypatch) -> None:
    class FakeStore:
        async def get_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            if session_id == "missing":
                return None
            return {"session_id": session_id}

    _snapshot = _make_snapshot(
        profile="## Preferences\n- Prefer concise answers.",
        summary="## Current Focus\n- Working on memory.",
        profile_updated_at="2026-03-13T12:10:00+08:00",
        summary_updated_at="2026-03-13T12:10:00+08:00",
    )

    class FakeMemoryService:
        async def refresh_from_session(self, session_id, language="en", owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return type("Result", (), {"changed": True})()

        def read_snapshot(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return _snapshot

    monkeypatch.setattr("deeptutor.api.routers.memory.get_sqlite_session_store", lambda: FakeStore())
    monkeypatch.setattr("deeptutor.api.routers.memory.get_memory_service", lambda: FakeMemoryService())

    app = _build_app()
    app.dependency_overrides[memory_module.get_current_user] = _teacher_user
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/memory/refresh",
            json={"session_id": "unified_1", "language": "en"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["changed"] is True
    assert "Working on memory" in body["summary"]
    assert "Prefer concise answers" in body["profile"]


def test_memory_router_updates_document(monkeypatch) -> None:
    class FakeMemoryService:
        def write_file(self, which, content: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return _make_snapshot(
                profile=content if which == "profile" else "",
                profile_updated_at="2026-03-13T12:20:00+08:00",
            )

    monkeypatch.setattr("deeptutor.api.routers.memory.get_memory_service", lambda: FakeMemoryService())

    app = _build_app()
    app.dependency_overrides[memory_module.get_current_user] = _teacher_user
    with TestClient(app) as client:
        response = client.put(
            "/api/v1/memory",
            json={"file": "profile", "content": "## Preferences\n- Prefer concise answers."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["saved"] is True
    assert body["profile"] == "## Preferences\n- Prefer concise answers."


def test_memory_router_clears_only_current_user_snapshot(monkeypatch) -> None:
    class FakeMemoryService:
        def clear_memory(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return _make_snapshot()

    monkeypatch.setattr("deeptutor.api.routers.memory.get_memory_service", lambda: FakeMemoryService())

    app = _build_app()
    app.dependency_overrides[memory_module.get_current_user] = _teacher_user
    with TestClient(app) as client:
        response = client.post("/api/v1/memory/clear", json={})

    assert response.status_code == 200
    assert response.json()["cleared"] is True
