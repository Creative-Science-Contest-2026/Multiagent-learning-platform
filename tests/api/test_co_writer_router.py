from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient


def _import_co_writer_module(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    config_path = tmp_path / "main.yaml"
    config_path.write_text("system:\n  language: en\npaths: {}\nlogging: {}\n", encoding="utf-8")
    monkeypatch.setattr(
        "deeptutor.services.config.loader.resolve_config_path",
        lambda _config_file, _project_root=None: (config_path, config_path.parent),
    )
    module = importlib.import_module("deeptutor.api.routers.co_writer")
    return importlib.reload(module)


def _build_app(co_writer_module) -> FastAPI:
    app = FastAPI()
    app.include_router(co_writer_module.router, prefix="/api/v1/co-writer")
    return app


def _user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"User {user_id}",
        role=role,
    )


def test_co_writer_routes_require_authentication(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    co_writer_module = _import_co_writer_module(monkeypatch, tmp_path)
    with TestClient(_build_app(co_writer_module)) as client:
        response = client.get("/api/v1/co-writer/history")

    assert response.status_code == 401


def test_co_writer_edit_injects_owner_metadata(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    co_writer_module = _import_co_writer_module(monkeypatch, tmp_path)
    captured = {}

    class FakeAgent:
        async def process(self, **kwargs):
            captured.update(kwargs)
            return {"edited_text": "done", "operation_id": "op-1"}

    monkeypatch.setattr(co_writer_module, "get_edit_agent", lambda: FakeAgent())
    app = _build_app(co_writer_module)
    app.dependency_overrides[co_writer_module.get_current_user] = lambda: _user()

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/co-writer/edit",
            json={"text": "abc", "instruction": "rewrite"},
        )

    assert response.status_code == 200
    assert captured["owner_user_id"] == "teacher-1"
    assert captured["owner_email"] == "teacher-1@example.com"


def test_co_writer_history_is_filtered_by_owner_scope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    co_writer_module = _import_co_writer_module(monkeypatch, tmp_path)
    captured = {}

    def fake_load_history(owner_user_id=None):
        captured["owner_user_id"] = owner_user_id
        return [{"id": "op-1", "owner_user_id": "teacher-1"}]

    monkeypatch.setattr(co_writer_module, "load_history", fake_load_history)
    app = _build_app(co_writer_module)
    app.dependency_overrides[co_writer_module.get_current_user] = lambda: _user()

    with TestClient(app) as client:
        response = client.get("/api/v1/co-writer/history")

    assert response.status_code == 200
    assert captured["owner_user_id"] == "teacher-1"
    assert response.json()["history"][0]["id"] == "op-1"


def test_co_writer_tool_call_lookup_respects_owner_scope(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    co_writer_module = _import_co_writer_module(monkeypatch, tmp_path)
    tool_calls_dir = tmp_path / "tool_calls"
    tool_calls_dir.mkdir(parents=True, exist_ok=True)
    (tool_calls_dir / "op-1_rag.json").write_text(
        json.dumps({"operation_id": "op-1", "owner_user_id": "teacher-1"}),
        encoding="utf-8",
    )
    (tool_calls_dir / "op-2_rag.json").write_text(
        json.dumps({"operation_id": "op-2", "owner_user_id": "teacher-2"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(co_writer_module, "TOOL_CALLS_DIR", tool_calls_dir)

    app = _build_app(co_writer_module)
    app.dependency_overrides[co_writer_module.get_current_user] = lambda: _user("teacher-1")
    with TestClient(app) as client:
        owned = client.get("/api/v1/co-writer/tool_calls/op-1")
        foreign = client.get("/api/v1/co-writer/tool_calls/op-2")

    assert owned.status_code == 200
    assert foreign.status_code == 404
