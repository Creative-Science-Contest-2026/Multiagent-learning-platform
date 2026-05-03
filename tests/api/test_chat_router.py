from __future__ import annotations

import importlib

import pytest
from fastapi import HTTPException

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


def _import_chat_module(monkeypatch: pytest.MonkeyPatch, tmp_path):
    config_path = tmp_path / "main.yaml"
    config_path.write_text("system:\n  language: en\npaths: {}\nlogging: {}\n", encoding="utf-8")
    monkeypatch.setattr(
        "deeptutor.services.config.loader.resolve_config_path",
        lambda _config_file, _project_root=None: (config_path, config_path.parent),
    )
    module = importlib.import_module("deeptutor.api.routers.chat")
    return importlib.reload(module)


def _build_app(chat_module) -> FastAPI:
    app = FastAPI()
    app.include_router(chat_module.router, prefix="/api/v1")
    return app


def _teacher_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        id="teacher-1",
        email="teacher@example.com",
        display_name="Teacher One",
        role="teacher",
    )


def test_chat_rest_routes_require_authentication(monkeypatch, tmp_path) -> None:
    chat_module = _import_chat_module(monkeypatch, tmp_path)

    with TestClient(_build_app(chat_module)) as client:
        response = client.get("/api/v1/chat/sessions")

    assert response.status_code == 401


def test_chat_rest_routes_are_owner_scoped(monkeypatch, tmp_path) -> None:
    chat_module = _import_chat_module(monkeypatch, tmp_path)
    class FakeManager:
        def list_sessions(self, limit=20, include_messages=False, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            assert include_messages is False
            return [{"session_id": "chat_1", "title": "Owned chat"}]

        def get_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            if session_id == "missing":
                return None
            return {"session_id": session_id, "title": "Owned chat", "messages": []}

        def delete_session(self, session_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return session_id == "chat_1"

    monkeypatch.setattr(chat_module, "session_manager", FakeManager())

    app = _build_app(chat_module)
    app.dependency_overrides[chat_module.get_current_user] = _teacher_user

    with TestClient(app) as client:
        list_response = client.get("/api/v1/chat/sessions", params={"limit": 5})
        get_response = client.get("/api/v1/chat/sessions/chat_1")
        missing_response = client.get("/api/v1/chat/sessions/missing")
        delete_response = client.delete("/api/v1/chat/sessions/chat_1")

    assert list_response.status_code == 200
    assert list_response.json()[0]["session_id"] == "chat_1"
    assert get_response.status_code == 200
    assert missing_response.status_code == 404
    assert delete_response.status_code == 200


def test_chat_websocket_requires_authenticated_cookie(monkeypatch, tmp_path) -> None:
    chat_module = _import_chat_module(monkeypatch, tmp_path)
    monkeypatch.setattr(
        chat_module,
        "get_current_user_from_websocket",
        lambda _ws: (_ for _ in ()).throw(HTTPException(status_code=401, detail="Authentication required")),
    )

    with TestClient(_build_app(chat_module)) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/chat"):
                pass
