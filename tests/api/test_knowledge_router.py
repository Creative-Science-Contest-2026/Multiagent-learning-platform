from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency in lightweight envs
    FastAPI = None
    TestClient = None

from deeptutor.services.auth.schemas import AuthenticatedUser

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")

knowledge_router_module = None
router = None


def _import_knowledge_router(monkeypatch, tmp_path: Path):
    if FastAPI is None or TestClient is None:  # pragma: no cover - guarded by pytestmark
        raise RuntimeError("fastapi is not installed")

    config_module = importlib.import_module("deeptutor.services.config")
    fake_settings_dir = tmp_path / "data" / "user" / "settings"
    fake_settings_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(config_module, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(
        config_module,
        "load_config_with_main",
        lambda *_args, **_kwargs: {"paths": {"user_log_dir": str(tmp_path / "logs")}},
    )

    sys.modules.pop("deeptutor.api.routers.knowledge", None)
    module = importlib.import_module("deeptutor.api.routers.knowledge")
    return module


def _teacher_user(user_id: str = "teacher-1", role: str = "teacher") -> AuthenticatedUser:
    return AuthenticatedUser(
        id=user_id,
        email=f"{user_id}@example.com",
        display_name=f"Teacher {user_id}",
        role=role,  # type: ignore[arg-type]
    )


def _build_app(
    knowledge_module,
    *,
    current_user: AuthenticatedUser | None = None,
    authenticated: bool = True,
) -> FastAPI:
    if FastAPI is None or knowledge_module is None:  # pragma: no cover - guarded by pytestmark
        raise RuntimeError("fastapi is not installed")
    app = FastAPI()
    app.include_router(knowledge_module.router, prefix="/api/v1/knowledge")
    if authenticated:
        app.dependency_overrides[knowledge_module.require_teacher_or_admin] = (
            lambda: current_user or _teacher_user()
        )
        app.dependency_overrides[knowledge_module.require_admin] = (
            lambda: _teacher_user("admin-1", role="admin")
        )
    return app


class _FakeKBManager:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.base_dir / "kb_config.json"
        self.config: dict[str, dict] = {"knowledge_bases": {}}

    def _load_config(self) -> dict:
        return self.config

    def _save_config(self) -> None:
        pass

    def list_knowledge_bases(self) -> list[str]:
        return sorted(self.config.get("knowledge_bases", {}).keys())

    def update_kb_status(self, name: str, status: str, progress: dict | None = None) -> None:
        entry = self.config.setdefault("knowledge_bases", {}).setdefault(name, {"path": name})
        entry["status"] = status
        entry["progress"] = progress or {}

    def get_knowledge_base_path(self, name: str) -> Path:
        kb_dir = self.base_dir / name
        kb_dir.mkdir(parents=True, exist_ok=True)
        return kb_dir

    def get_default(self) -> str | None:
        return self.config.get("default_kb")

    def set_default(self, name: str) -> None:
        self.config["default_kb"] = name

    def delete_knowledge_base(self, name: str, confirm: bool = False) -> bool:
        if name not in self.config.get("knowledge_bases", {}):
            raise ValueError(name)
        if not confirm:
            return False
        self.config.get("knowledge_bases", {}).pop(name, None)
        return True

    def get_info(self, name: str) -> dict:
        if name not in self.config.get("knowledge_bases", {}):
            raise ValueError(name)
        entry = self.config["knowledge_bases"][name]
        return {
            "name": name,
            "is_default": name == self.get_default(),
            "statistics": {"raw_documents": 1},
            "status": entry.get("status"),
            "progress": entry.get("progress"),
            "metadata": entry.get("metadata"),
        }


class _FakeInitializer:
    def __init__(self, kb_name: str, base_dir: str, **_kwargs) -> None:
        self.kb_name = kb_name
        self.base_dir = base_dir
        self.kb_dir = Path(base_dir) / kb_name
        self.raw_dir = self.kb_dir / "raw"
        self.progress_tracker = _kwargs.get("progress_tracker")

    def create_directory_structure(self) -> None:
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def _register_to_config(self) -> None:
        pass


def _upload_payload() -> list[tuple[str, tuple[str, bytes, str]]]:
    return [("files", ("demo.txt", b"hello", "text/plain"))]


def test_rag_providers_returns_llamaindex_only() -> None:
    with pytest.MonkeyPatch.context() as monkeypatch:
        knowledge_module = _import_knowledge_router(monkeypatch, Path.cwd())

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/rag-providers")

    assert response.status_code == 200
    payload = response.json()
    assert payload == {
        "providers": [
            {
                "id": "llamaindex",
                "name": "LlamaIndex",
                "description": "Pure vector retrieval, fastest processing speed.",
            }
        ]
    }


def test_knowledge_routes_require_authenticated_teacher_surface(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    with TestClient(_build_app(knowledge_module, authenticated=False)) as client:
        response = client.get("/api/v1/knowledge/list")

    assert response.status_code == 401


def test_list_knowledge_bases_filters_owned_entries(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["owned-kb"] = {
        "path": "owned-kb",
        "status": "ready",
        "owner_user_id": "teacher-1",
        "owner": "Teacher teacher-1",
    }
    manager.config["knowledge_bases"]["other-kb"] = {
        "path": "other-kb",
        "status": "ready",
        "owner_user_id": "teacher-2",
        "owner": "Teacher teacher-2",
    }
    manager.config["knowledge_bases"]["legacy-kb"] = {
        "path": "legacy-kb",
        "status": "ready",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module, current_user=_teacher_user("teacher-1"))) as client:
        response = client.get("/api/v1/knowledge/list")

    assert response.status_code == 200
    names = [row["name"] for row in response.json()]
    assert "owned-kb" in names
    assert "legacy-kb" in names
    assert "other-kb" not in names


def test_default_knowledge_base_is_user_specific(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["kb-a"] = {
        "path": "kb-a",
        "status": "ready",
        "owner_user_id": "teacher-1",
    }
    manager.config["knowledge_bases"]["kb-b"] = {
        "path": "kb-b",
        "status": "ready",
        "owner_user_id": "teacher-2",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module, current_user=_teacher_user("teacher-1"))) as client:
        set_response = client.put("/api/v1/knowledge/default/kb-a")
        get_response = client.get("/api/v1/knowledge/default")

    assert set_response.status_code == 200
    assert get_response.status_code == 200
    assert get_response.json() == {"default_kb": "kb-a"}
    assert manager.config["user_defaults"]["teacher-1"] == "kb-a"


def test_create_kb_does_not_require_llm_precheck(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "KnowledgeBaseInitializer", _FakeInitializer)
    monkeypatch.setattr(knowledge_module, "get_llm_config", lambda: (_ for _ in ()).throw(RuntimeError("should not be called")), raising=False)

    async def _noop_init_task(*_args, **_kwargs):
        return None

    monkeypatch.setattr(knowledge_module, "run_initialization_task", _noop_init_task)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/create",
            data={"name": "kb-new", "rag_provider": "llamaindex"},
            files=_upload_payload(),
        )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "kb-new"
    assert isinstance(body.get("task_id"), str) and body["task_id"]
    assert manager.config["knowledge_bases"]["kb-new"]["rag_provider"] == "llamaindex"
    assert manager.config["knowledge_bases"]["kb-new"]["needs_reindex"] is False
    assert manager.config["knowledge_bases"]["kb-new"]["owner_user_id"] == "teacher-1"
    assert manager.config["user_defaults"]["teacher-1"] == "kb-new"


def test_create_kb_defaults_to_system_provider_when_request_omits_provider(
    monkeypatch, tmp_path: Path
) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "KnowledgeBaseInitializer", _FakeInitializer)

    async def _noop_init_task(*_args, **_kwargs):
        return None

    monkeypatch.setattr(knowledge_module, "run_initialization_task", _noop_init_task)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/create",
            data={"name": "kb-default-provider"},
            files=_upload_payload(),
        )

    assert response.status_code == 200
    assert (
        manager.config["knowledge_bases"]["kb-default-provider"]["rag_provider"] == "llamaindex"
    )


def test_create_rejects_unregistered_provider(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/create",
            data={"name": "kb-invalid", "rag_provider": "lightrag"},
            files=_upload_payload(),
        )

    assert response.status_code == 400
    assert "Unsupported RAG provider" in response.json()["detail"]


def test_upload_returns_409_when_kb_needs_reindex(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["legacy-kb"] = {
        "path": "legacy-kb",
        "rag_provider": "llamaindex",
        "needs_reindex": True,
        "status": "needs_reindex",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/legacy-kb/upload", files=_upload_payload())

    assert response.status_code == 409
    assert "needs reindex" in response.json()["detail"].lower()


def test_upload_ready_kb_returns_task_id(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["ready-kb"] = {
        "path": "ready-kb",
        "rag_provider": "llamaindex",
        "needs_reindex": False,
        "status": "ready",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    async def _noop_upload_task(*_args, **_kwargs):
        return None

    monkeypatch.setattr(knowledge_module, "run_upload_processing_task", _noop_upload_task)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/ready-kb/upload", files=_upload_payload())

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("task_id"), str) and body["task_id"]


def test_update_config_rejects_unregistered_provider() -> None:
    class _FakeConfigService:
        def set_kb_config(self, kb_name: str, config: dict) -> None:
            self.kb_name = kb_name
            self.config = config

        def get_kb_config(self, _kb_name: str) -> dict:
            return {"rag_provider": "llamaindex"}

    fake_service = _FakeConfigService()

    config_module = importlib.import_module("deeptutor.services.config")
    with pytest.MonkeyPatch.context() as monkeypatch:
        knowledge_module = _import_knowledge_router(monkeypatch, Path.cwd())
        monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)
        with TestClient(_build_app(knowledge_module)) as client:
            response = client.put(
                "/api/v1/knowledge/demo/config",
                json={"rag_provider": "raganything"},
            )

    assert response.status_code == 400
    assert "Unsupported RAG provider" in response.json()["detail"]


def test_update_config_persists_teacher_pack_metadata(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {
                "demo": {
                    "rag_provider": "llamaindex",
                    "subject": "Old",
                }
            }

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")

    payload = {
        "subject": "Math",
        "grade": "10",
        "curriculum": "Vietnam National Curriculum",
        "learning_objectives": ["Quadratic equations", "Graph reading"],
        "owner": "teacher-a",
        "sharing_status": "private",
        "team_members": ["teacher-a", "teacher-b"],
        "pending_invites": ["invite@example.com"],
    }

    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/demo/config", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["config"]["subject"] == "Math"
    assert body["config"]["grade"] == "10"
    assert body["config"]["curriculum"] == "Vietnam National Curriculum"
    assert body["config"]["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert body["config"]["owner"] == "teacher-a"
    assert body["config"]["sharing_status"] == "private"
    assert body["config"]["team_members"] == ["teacher-a", "teacher-b"]
    assert body["config"]["pending_invites"] == ["invite@example.com"]


def test_update_config_persists_extended_teacher_pack_metadata(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {
                "demo": {
                    "rag_provider": "llamaindex",
                }
            }

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")

    payload = {
        "tags": ["algebra", "geometry"],
        "difficulty": "intermediate",
        "language": "Vietnamese",
        "estimated_hours": 12.5,
        "prerequisites": ["Basic math"],
        "content_types": ["text", "images"],
    }

    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/demo/config", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["config"]["tags"] == ["algebra", "geometry"]
    assert body["config"]["difficulty"] == "intermediate"
    assert body["config"]["language"] == "Vietnamese"
    assert body["config"]["estimated_hours"] == 12.5
    assert body["config"]["prerequisites"] == ["Basic math"]
    assert body["config"]["content_types"] == ["text", "images"]


def test_get_knowledge_base_details_exposes_teacher_pack_metadata(
    monkeypatch, tmp_path: Path
) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    kb_root = tmp_path / "knowledge_bases"
    kb_dir = kb_root / "demo"
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)

    manager_module = importlib.import_module("deeptutor.knowledge.manager")
    manager = manager_module.KnowledgeBaseManager(base_dir=str(kb_root))
    manager.config = {
        "knowledge_bases": {
            "demo": {
                "path": "demo",
                "description": "Knowledge base: demo",
                "rag_provider": "llamaindex",
                "subject": "Math",
                "grade": "10",
                "curriculum": "Vietnam National Curriculum",
                "learning_objectives": ["Quadratic equations", "Graph reading"],
                "owner": "teacher-a",
                "sharing_status": "private",
                "team_members": ["teacher-a", "teacher-b"],
                "pending_invites": ["invite@example.com"],
                "status": "ready",
            }
        }
    }
    manager._save_config()

    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/demo")

    assert response.status_code == 200
    metadata = response.json()["metadata"]
    assert metadata["subject"] == "Math"
    assert metadata["grade"] == "10"
    assert metadata["curriculum"] == "Vietnam National Curriculum"
    assert metadata["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert metadata["owner"] == "teacher-a"
    assert metadata["sharing_status"] == "private"
    assert metadata["team_members"] == ["teacher-a", "teacher-b"]
    assert metadata["pending_invites"] == ["invite@example.com"]


def test_list_knowledge_bases_includes_teacher_pack_metadata(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _MetadataAwareManager(_FakeKBManager):
        def get_default(self) -> str | None:
            return "demo"

        def get_info(self, name: str) -> dict:
            return {
                "name": name,
                "is_default": True,
                "statistics": {"raw_documents": 1},
                "status": "ready",
                "progress": None,
                "metadata": {
                    "subject": "Math",
                    "grade": "10",
                    "curriculum": "Vietnam National Curriculum",
                    "learning_objectives": ["Quadratic equations"],
                    "owner": "teacher-a",
                    "sharing_status": "private",
                    "team_members": ["teacher-a", "teacher-b"],
                    "pending_invites": ["invite@example.com"],
                },
            }

    manager = _MetadataAwareManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["demo"] = {"path": "demo"}
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/list")

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["metadata"]["subject"] == "Math"
    assert payload[0]["metadata"]["grade"] == "10"
    assert payload[0]["metadata"]["owner"] == "teacher-a"
    assert payload[0]["metadata"]["team_members"] == ["teacher-a", "teacher-b"]
    assert payload[0]["metadata"]["pending_invites"] == ["invite@example.com"]


def test_list_knowledge_bases_falls_back_to_progress_file_when_config_progress_missing(
    monkeypatch, tmp_path: Path
) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    manager_module = importlib.import_module("deeptutor.knowledge.manager")
    kb_base_dir = tmp_path / "knowledge_bases"
    kb_dir = kb_base_dir / "demo-kb"
    kb_dir.mkdir(parents=True, exist_ok=True)
    (kb_dir / ".progress.json").write_text(
        json.dumps(
            {
                "kb_name": "demo-kb",
                "stage": "completed",
                "message": "Knowledge base initialization complete!",
                "progress_percent": 100,
                "task_id": "task-abc",
                "timestamp": "2026-04-30T13:00:00",
            }
        ),
        encoding="utf-8",
    )

    manager = manager_module.KnowledgeBaseManager(base_dir=str(kb_base_dir))
    manager.config = {
        "knowledge_bases": {
            "demo-kb": {
                "path": "demo-kb",
                "description": "Knowledge base: demo-kb",
                "rag_provider": "llamaindex",
            }
        }
    }
    manager._save_config()

    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/list")

    assert response.status_code == 200
    payload = response.json()
    assert payload[0]["status"] == "ready"
    assert payload[0]["progress"]["stage"] == "completed"
    assert payload[0]["progress"]["progress_percent"] == 100


def test_update_config_rejects_invalid_sharing_status(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {"demo": {"rag_provider": "llamaindex"}}

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put(
            "/api/v1/knowledge/demo/config",
            json={"sharing_status": "school"},
        )

    assert response.status_code == 400
    assert "sharing_status" in response.json()["detail"]


def test_update_config_normalizes_learning_objectives(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {"demo": {"rag_provider": "llamaindex"}}

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return self.store.get(kb_name, {})

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    payload = {
        "learning_objectives": ["  Quadratic equations  ", "", "  ", "Graph reading"],
        "owner": " teacher-a ",
        "team_members": [" teacher-a ", " ", "teacher-b "],
        "pending_invites": [" invite@example.com ", "", "reviewer@example.com "],
    }

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/demo/config", json=payload)

    assert response.status_code == 200
    config = response.json()["config"]
    assert config["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert config["owner"] == "teacher-a"
    assert config["team_members"] == ["teacher-a", "teacher-b"]
    assert config["pending_invites"] == ["invite@example.com", "reviewer@example.com"]


def test_update_config_appends_teacher_pack_version_history(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {
                "demo": {
                    "rag_provider": "llamaindex",
                    "subject": "Math",
                    "grade": "10",
                    "owner": "teacher-a",
                }
            }

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return dict(self.store.get(kb_name, {}))

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put(
            "/api/v1/knowledge/demo/config",
            json={
                "subject": "Advanced Math",
                "grade": "10",
                "owner": "teacher-a",
                "learning_objectives": ["Quadratic equations"],
            },
        )

    assert response.status_code == 200
    config = response.json()["config"]
    assert config["current_version"] == 2
    assert len(config["version_history"]) == 1
    revision = config["version_history"][0]
    assert revision["version"] == 2
    assert revision["changed_fields"] == ["learning_objectives", "subject"]


def test_update_config_starts_teacher_pack_version_history_at_one(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def __init__(self) -> None:
            self.store = {"demo": {"rag_provider": "llamaindex"}}

        def set_kb_config(self, kb_name: str, config: dict) -> None:
            current = self.store.get(kb_name, {})
            current.update(config)
            self.store[kb_name] = current

        def get_kb_config(self, kb_name: str) -> dict:
            return dict(self.store.get(kb_name, {}))

    fake_service = _FakeConfigService()
    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: fake_service)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put(
            "/api/v1/knowledge/demo/config",
            json={
                "subject": "Math",
                "owner": "teacher-a",
            },
        )

    assert response.status_code == 200
    config = response.json()["config"]
    assert config["current_version"] == 1
    assert config["version_history"][0]["version"] == 1
    assert config["version_history"][0]["changed_fields"] == ["owner", "subject"]


def test_get_all_and_single_kb_configs(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)

    class _FakeConfigService:
        def get_all_configs(self) -> dict:
            return {"demo-kb": {"subject": "Math"}}

        def get_kb_config(self, kb_name: str) -> dict:
            return {"name": kb_name, "subject": "Math"}

    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: _FakeConfigService())

    with TestClient(_build_app(knowledge_module)) as client:
        all_response = client.get("/api/v1/knowledge/configs")
        single_response = client.get("/api/v1/knowledge/demo-kb/config")

    assert all_response.status_code == 200
    assert all_response.json() == {"demo-kb": {"subject": "Math"}}
    assert single_response.status_code == 200
    assert single_response.json() == {
        "kb_name": "demo-kb",
        "config": {"name": "demo-kb", "subject": "Math"},
    }


def test_sync_configs_from_metadata_returns_success(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    calls: list[Path] = []

    class _FakeConfigService:
        def sync_all_from_metadata(self, base_dir: Path) -> None:
            calls.append(base_dir)

    config_module = importlib.import_module("deeptutor.services.config")
    monkeypatch.setattr(config_module, "get_kb_config_service", lambda: _FakeConfigService())
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/configs/sync")

    assert response.status_code == 200
    assert calls == [tmp_path / "knowledge_bases"]
    assert response.json()["status"] == "success"


def test_get_knowledge_base_details_returns_404_for_missing_kb(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.get("/api/v1/knowledge/missing-kb")

    assert response.status_code == 404
    assert "missing-kb" in response.json()["detail"]


def test_delete_knowledge_base_returns_404_for_missing_kb(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.delete("/api/v1/knowledge/missing-kb")

    assert response.status_code == 404
    assert "missing-kb" in response.json()["detail"]


def test_upload_rejects_provider_mismatch(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["demo-kb"] = {
        "path": "demo-kb",
        "rag_provider": "llamaindex",
        "needs_reindex": False,
        "status": "ready",
    }
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")
    monkeypatch.setattr(
        knowledge_module,
        "has_pipeline",
        lambda provider: provider in {"llamaindex", "basic-rag"},
    )
    monkeypatch.setattr(knowledge_module, "normalize_provider_name", lambda provider: provider)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post(
            "/api/v1/knowledge/demo-kb/upload",
            data={"rag_provider": "basic-rag"},
            files=_upload_payload(),
        )

    assert response.status_code == 400
    assert "does not match KB provider" in response.json()["detail"]


def test_get_and_set_default_kb(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["demo-kb"] = {"path": "demo-kb"}
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        initial = client.get("/api/v1/knowledge/default")
        updated = client.put("/api/v1/knowledge/default/demo-kb")
        final_state = client.get("/api/v1/knowledge/default")

    assert initial.status_code == 200
    assert initial.json() == {"default_kb": None}
    assert updated.status_code == 200
    assert updated.json() == {"status": "success", "default_kb": "demo-kb"}
    assert final_state.json() == {"default_kb": "demo-kb"}


def test_set_default_kb_returns_404_for_unknown_kb(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.put("/api/v1/knowledge/default/missing-kb")

    assert response.status_code == 404
    assert "missing-kb" in response.json()["detail"]


def test_clear_progress_resets_tracker_file(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    monkeypatch.setattr(knowledge_module, "_kb_base_dir", tmp_path / "knowledge_bases")

    tracker = knowledge_module.ProgressTracker("demo-kb", knowledge_module._kb_base_dir)
    tracker.update(
        knowledge_module.ProgressStage.PROCESSING_DOCUMENTS,
        "processing",
        current=1,
        total=1,
    )

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.post("/api/v1/knowledge/demo-kb/progress/clear")
        after = client.get("/api/v1/knowledge/demo-kb/progress")

    assert response.status_code == 200
    assert after.json() == {"status": "not_started", "message": "Initialization not started"}


def test_delete_knowledge_base_removes_existing_kb(monkeypatch, tmp_path: Path) -> None:
    knowledge_module = _import_knowledge_router(monkeypatch, tmp_path)
    manager = _FakeKBManager(tmp_path / "knowledge_bases")
    manager.config["knowledge_bases"]["demo-kb"] = {"path": "demo-kb"}
    monkeypatch.setattr(knowledge_module, "get_kb_manager", lambda: manager)

    with TestClient(_build_app(knowledge_module)) as client:
        response = client.delete("/api/v1/knowledge/demo-kb")

    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    assert "demo-kb" not in manager.config["knowledge_bases"]
