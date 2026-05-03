from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from fastapi import HTTPException

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


def _import_guide_module(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    config_path = tmp_path / "main.yaml"
    config_path.write_text("system:\n  language: en\npaths: {}\nlogging: {}\n", encoding="utf-8")
    monkeypatch.setattr(
        "deeptutor.services.config.loader.resolve_config_path",
        lambda _config_file, _project_root=None: (config_path, config_path.parent),
    )
    module = importlib.import_module("deeptutor.api.routers.guide")
    return importlib.reload(module)


def _build_app(guide_module) -> FastAPI:
    app = FastAPI()
    app.include_router(guide_module.router, prefix="/api/v1/guide")
    return app


def _teacher_user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"Teacher {user_id}",
        role=role,
    )


def test_guide_routes_require_authentication(monkeypatch, tmp_path) -> None:
    guide_module = _import_guide_module(monkeypatch, tmp_path)

    with TestClient(_build_app(guide_module)) as client:
        response = client.get("/api/v1/guide/sessions")

    assert response.status_code == 401


def test_guide_routes_forward_owner_scope(monkeypatch, tmp_path) -> None:
    guide_module = _import_guide_module(monkeypatch, tmp_path)

    class FakeManager:
        async def create_session(self, user_input: str, display_title=None, notebook_context="", owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True, "session_id": "guide-1"}

        async def start_learning(self, session_id: str, owner_user_id=None):
            assert session_id == "guide-1"
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def navigate_to_knowledge(self, session_id: str, knowledge_index: int, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def complete_learning(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def chat(self, session_id: str, message: str, knowledge_index=None, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True, "answer": "ok"}

        async def fix_html(self, session_id: str, bug_description: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def retry_page(self, session_id: str, page_index: int, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def reset_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        async def delete_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"success": True}

        def list_sessions(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return [{"session_id": "guide-1"}]

        def get_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            if session_id == "missing":
                return None
            return {"session_id": session_id}

        def get_current_html(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return "<p>ok</p>"

        def get_session_pages(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"session_id": session_id, "page_statuses": {}}

    monkeypatch.setattr(guide_module, "get_guide_manager", lambda: FakeManager())
    app = _build_app(guide_module)
    app.dependency_overrides[guide_module.get_current_user] = lambda: _teacher_user()

    with TestClient(app) as client:
        assert client.post("/api/v1/guide/create_session", json={"user_input": "fractions"}).status_code == 200
        assert client.post("/api/v1/guide/start", json={"session_id": "guide-1"}).status_code == 200
        assert client.post("/api/v1/guide/navigate", json={"session_id": "guide-1", "knowledge_index": 0}).status_code == 200
        assert client.post("/api/v1/guide/complete", json={"session_id": "guide-1"}).status_code == 200
        assert client.post("/api/v1/guide/chat", json={"session_id": "guide-1", "message": "hi"}).status_code == 200
        assert client.post("/api/v1/guide/fix_html", json={"session_id": "guide-1", "bug_description": "bug"}).status_code == 200
        assert client.post("/api/v1/guide/retry_page", json={"session_id": "guide-1", "page_index": 0}).status_code == 200
        assert client.post("/api/v1/guide/reset", json={"session_id": "guide-1"}).status_code == 200
        assert client.delete("/api/v1/guide/session/guide-1").status_code == 200
        assert client.get("/api/v1/guide/sessions").status_code == 200
        assert client.get("/api/v1/guide/session/guide-1").status_code == 200
        assert client.get("/api/v1/guide/session/missing").status_code == 404
        assert client.get("/api/v1/guide/session/guide-1/html").status_code == 200
        assert client.get("/api/v1/guide/session/guide-1/pages").status_code == 200


def test_guide_websocket_requires_authenticated_cookie(monkeypatch, tmp_path) -> None:
    guide_module = _import_guide_module(monkeypatch, tmp_path)
    monkeypatch.setattr(
        guide_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app(guide_module)) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/guide/ws/guide-1"):
                pass
