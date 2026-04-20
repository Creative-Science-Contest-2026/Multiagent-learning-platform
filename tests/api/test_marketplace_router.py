from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from deeptutor.api.routers import marketplace


class _FakeKBManager:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.config = {
            "knowledge_bases": {
                "shared-pack": {
                    "path": "shared-pack",
                    "description": "Shared pack",
                    "sharing_status": "public",
                    "subject": "Math",
                    "grade": "8",
                    "curriculum": "National",
                    "learning_objectives": ["Linear equations", "Word problems"],
                    "owner": "Teacher A",
                    "created_at": "2026-04-20T00:00:00",
                    "updated_at": "2026-04-20T00:00:00",
                },
                "private-pack": {
                    "path": "private-pack",
                    "description": "Private pack",
                    "sharing_status": "private",
                    "subject": "Math",
                    "owner": "Teacher B",
                },
            }
        }

    def list_knowledge_bases(self) -> list[str]:
        return list(self.config.get("knowledge_bases", {}).keys())

    def get_info(self, name: str) -> dict:
        kb = self.config["knowledge_bases"][name]
        return {
            "name": name,
            "is_default": False,
            "status": "ready",
            "statistics": {"content_lists": 3},
            "metadata": {
                "subject": kb.get("subject"),
                "grade": kb.get("grade"),
                "curriculum": kb.get("curriculum"),
                "learning_objectives": kb.get("learning_objectives", []),
                "owner": kb.get("owner"),
                "sharing_status": kb.get("sharing_status"),
            },
        }

    def _load_config(self) -> dict:
        return self.config

    def _save_config(self) -> None:
        return


def _build_app(monkeypatch, tmp_path: Path) -> TestClient:
    (tmp_path / "shared-pack").mkdir(parents=True)
    (tmp_path / "shared-pack" / "raw").mkdir(parents=True)
    (tmp_path / "shared-pack" / "rag_storage").mkdir(parents=True)
    (tmp_path / "shared-pack" / "raw" / "lesson-1.md").write_text("Lesson 1", encoding="utf-8")
    (tmp_path / "shared-pack" / "raw" / "lesson-2.md").write_text("Lesson 2", encoding="utf-8")
    (tmp_path / "shared-pack" / "raw" / "lesson-3.md").write_text("Lesson 3", encoding="utf-8")
    (tmp_path / "shared-pack" / "raw" / "lesson-4.md").write_text("Lesson 4", encoding="utf-8")

    manager = _FakeKBManager(tmp_path)
    monkeypatch.setattr("deeptutor.api.routers.marketplace.get_kb_manager", lambda: manager)

    app = FastAPI()
    app.include_router(marketplace.router, prefix="/api/v1/marketplace")
    return TestClient(app)


def test_marketplace_list_only_returns_shareable_packs(monkeypatch, tmp_path: Path) -> None:
    client = _build_app(monkeypatch, tmp_path)

    response = client.get("/api/v1/marketplace/list")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["packs"][0]["name"] == "shared-pack"
    assert payload["packs"][0]["sharing_status"] == "public"


def test_marketplace_import_copies_pack_and_registers_new_entry(monkeypatch, tmp_path: Path) -> None:
    client = _build_app(monkeypatch, tmp_path)

    response = client.post("/api/v1/marketplace/import/shared-pack")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["pack"]["name"] == "shared-pack__imported"

    imported_path = tmp_path / "shared-pack__imported"
    assert imported_path.exists()
    assert (imported_path / "raw").exists()
    assert (imported_path / "rag_storage").exists()


def test_marketplace_preview_returns_compact_pack_summary(monkeypatch, tmp_path: Path) -> None:
    client = _build_app(monkeypatch, tmp_path)

    response = client.get("/api/v1/marketplace/shared-pack/preview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "shared-pack"
    assert payload["description"] == "Shared pack"
    assert payload["document_count"] == 4
    assert payload["sample_documents"] == ["lesson-1.md", "lesson-2.md", "lesson-3.md"]
    assert payload["learning_objectives"] == ["Linear equations", "Word problems"]
