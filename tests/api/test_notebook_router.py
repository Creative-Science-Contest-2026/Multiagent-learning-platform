from __future__ import annotations

import importlib

import pytest

from deeptutor.services.auth.schemas import AuthenticatedUser

pytest.importorskip("fastapi")

FastAPI = pytest.importorskip("fastapi").FastAPI
TestClient = pytest.importorskip("fastapi.testclient").TestClient
notebook_module = importlib.import_module("deeptutor.api.routers.notebook")


def _build_app() -> FastAPI:
    app = FastAPI()
    app.include_router(notebook_module.router, prefix="/api/v1/notebook")
    return app


def _user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"User {user_id}",
        role=role,
    )


def test_notebook_routes_require_authentication() -> None:
    with TestClient(_build_app()) as client:
        response = client.get("/api/v1/notebook/list")

    assert response.status_code == 401


def test_notebook_routes_forward_owner_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeManager:
        def list_notebooks(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return [{"id": "nb-1"}]

        def get_statistics(self, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return {"total_notebooks": 1}

        def create_notebook(self, **kwargs):
            assert kwargs["owner_user_id"] == "teacher-1"
            assert kwargs["owner_email"] == "teacher-1@example.com"
            return {"id": "nb-1"}

        def get_notebook(self, notebook_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            if notebook_id == "missing":
                return None
            return {"id": notebook_id}

        def update_notebook(self, **kwargs):
            assert kwargs["owner_user_id"] == "teacher-1"
            return {"id": kwargs["notebook_id"]}

        def delete_notebook(self, notebook_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return notebook_id == "nb-1"

        def add_record(self, **kwargs):
            assert kwargs["owner_user_id"] == "teacher-1"
            return {"record": {"id": "rec-1"}, "added_to_notebooks": kwargs["notebook_ids"]}

        def remove_record(self, notebook_id: str, record_id: str, owner_user_id=None):
            assert owner_user_id == "teacher-1"
            return True

        def update_record(self, **kwargs):
            assert kwargs["owner_user_id"] == "teacher-1"
            return {"id": kwargs["record_id"]}

    monkeypatch.setattr(notebook_module, "notebook_manager", FakeManager())
    app = _build_app()
    app.dependency_overrides[notebook_module.get_current_user] = lambda: _user()

    with TestClient(app) as client:
        assert client.get("/api/v1/notebook/list").status_code == 200
        assert client.get("/api/v1/notebook/statistics").status_code == 200
        assert client.post("/api/v1/notebook/create", json={"name": "Notebook"}).status_code == 200
        assert client.get("/api/v1/notebook/nb-1").status_code == 200
        assert client.get("/api/v1/notebook/missing").status_code == 404
        assert client.put("/api/v1/notebook/nb-1", json={"name": "Updated"}).status_code == 200
        assert client.delete("/api/v1/notebook/nb-1").status_code == 200
        assert client.post(
            "/api/v1/notebook/add_record",
            json={
                "notebook_ids": ["nb-1"],
                "record_type": "chat",
                "title": "Hello",
                "summary": "Short summary",
                "user_query": "Hi",
                "output": "There",
            },
        ).status_code == 200
        assert client.delete("/api/v1/notebook/nb-1/records/rec-1").status_code == 200
        assert client.put(
            "/api/v1/notebook/nb-1/records/rec-1",
            json={"title": "Updated record"},
        ).status_code == 200
