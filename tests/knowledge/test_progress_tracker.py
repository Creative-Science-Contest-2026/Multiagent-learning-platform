from __future__ import annotations

from deeptutor.knowledge.progress_tracker import ProgressStage, ProgressTracker


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
