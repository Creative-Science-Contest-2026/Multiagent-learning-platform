from __future__ import annotations

from deeptutor.knowledge.manager import KnowledgeBaseManager


def test_get_info_normalizes_teacher_pack_metadata(tmp_path) -> None:
    kb_root = tmp_path / "knowledge_bases"
    kb_dir = kb_root / "demo"
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)

    manager = KnowledgeBaseManager(base_dir=str(kb_root))
    manager.config = {
        "knowledge_bases": {
            "demo": {
                "path": "demo",
                "description": "Knowledge base: demo",
                "rag_provider": "llamaindex",
                "subject": "  Math  ",
                "grade": "  10  ",
                "curriculum": "  Vietnam National Curriculum  ",
                "learning_objectives": ["  Quadratic equations  ", "", "Graph reading"],
                "owner": "  teacher-a  ",
                "sharing_status": "  private  ",
                "team_members": [" teacher-a ", "", " teacher-b "],
                "pending_invites": [" invite1@example.com ", " ", "invite2@example.com"],
                "status": "ready",
            }
        }
    }
    manager._save_config()

    info = manager.get_info("demo")
    metadata = info["metadata"]

    assert metadata["subject"] == "Math"
    assert metadata["grade"] == "10"
    assert metadata["curriculum"] == "Vietnam National Curriculum"
    assert metadata["learning_objectives"] == ["Quadratic equations", "Graph reading"]
    assert metadata["owner"] == "teacher-a"
    assert metadata["sharing_status"] == "private"
    assert metadata["team_members"] == ["teacher-a", "teacher-b"]
    assert metadata["pending_invites"] == ["invite1@example.com", "invite2@example.com"]


def test_get_info_normalizes_version_history_metadata(tmp_path) -> None:
    kb_root = tmp_path / "knowledge_bases"
    kb_dir = kb_root / "demo"
    (kb_dir / "llamaindex_storage").mkdir(parents=True, exist_ok=True)

    manager = KnowledgeBaseManager(base_dir=str(kb_root))
    manager.config = {
        "knowledge_bases": {
            "demo": {
                "path": "demo",
                "description": "Knowledge base: demo",
                "rag_provider": "llamaindex",
                "current_version": 3,
                "version_history": [
                    {
                        "version": 2,
                        "updated_at": "2026-04-24T15:00:00Z",
                        "changed_fields": [" subject ", "", "learning_objectives"],
                    },
                    {
                        "version": "3",
                        "updated_at": "2026-04-24T15:30:00Z",
                        "changed_fields": [" owner "],
                    },
                ],
                "status": "ready",
            }
        }
    }
    manager._save_config()

    info = manager.get_info("demo")
    metadata = info["metadata"]

    assert metadata["current_version"] == 3
    assert metadata["version_history"] == [
        {
            "version": 2,
            "updated_at": "2026-04-24T15:00:00Z",
            "changed_fields": ["subject", "learning_objectives"],
        },
        {
            "version": 3,
            "updated_at": "2026-04-24T15:30:00Z",
            "changed_fields": ["owner"],
        },
    ]
