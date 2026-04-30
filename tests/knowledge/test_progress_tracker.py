from __future__ import annotations

from deeptutor.knowledge.manager import KnowledgeBaseManager
from deeptutor.knowledge.progress_tracker import ProgressStage, ProgressTracker
from deeptutor.services.config.knowledge_base_config import KnowledgeBaseConfigService


def test_progress_tracker_persists_file_statuses_in_kb_progress(tmp_path) -> None:
    tracker = ProgressTracker("demo-kb", tmp_path)

    tracker.update(
        ProgressStage.PROCESSING_FILE,
        "Indexing documents",
        current=1,
        total=2,
        file_name="chapter-1.pdf",
        file_statuses=[
            {
                "name": "chapter-1.pdf",
                "status": "indexed",
                "updated_at": "2026-04-30T09:00:00",
            },
            {
                "name": "chapter-2.pdf",
                "status": "processing",
                "updated_at": "2026-04-30T09:00:03",
            },
        ],
    )

    progress = tracker.get_progress()

    assert progress is not None
    assert progress["file_statuses"] == [
        {
            "name": "chapter-1.pdf",
            "status": "indexed",
            "updated_at": "2026-04-30T09:00:00",
        },
        {
            "name": "chapter-2.pdf",
            "status": "processing",
            "updated_at": "2026-04-30T09:00:03",
        },
    ]


def test_set_kb_config_preserves_existing_runtime_status_and_progress(tmp_path) -> None:
    kb_base_dir = tmp_path / "knowledge_bases"
    kb_base_dir.mkdir(parents=True, exist_ok=True)

    service = KnowledgeBaseConfigService(config_path=kb_base_dir / "kb_config.json")
    manager = KnowledgeBaseManager(base_dir=str(kb_base_dir))
    manager.update_kb_status(
        name="demo-kb",
        status="ready",
        progress={
            "stage": "completed",
            "message": "Indexed successfully",
            "percent": 100,
            "task_id": "task-123",
        },
    )

    service.set_kb_config(
        "demo-kb",
        {
            "subject": "Toán",
            "difficulty": "beginner",
        },
    )

    reloaded = KnowledgeBaseManager(base_dir=str(kb_base_dir)).get_info("demo-kb")

    assert reloaded["status"] == "ready"
    assert reloaded["progress"]["stage"] == "completed"
    assert reloaded["progress"]["percent"] == 100
