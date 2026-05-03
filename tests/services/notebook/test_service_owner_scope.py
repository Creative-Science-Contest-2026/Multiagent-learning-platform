from __future__ import annotations

from deeptutor.services.notebook.service import NotebookManager


def test_notebook_manager_filters_by_owner(tmp_path) -> None:
    manager = NotebookManager(str(tmp_path))

    teacher_one = manager.create_notebook(
        "Teacher One",
        owner_user_id="teacher-1",
        owner_email="teacher-1@example.com",
        owner_display_name="Teacher One",
    )
    teacher_two = manager.create_notebook(
        "Teacher Two",
        owner_user_id="teacher-2",
        owner_email="teacher-2@example.com",
        owner_display_name="Teacher Two",
    )

    manager.add_record(
        [teacher_one["id"]],
        "chat",
        "First",
        "Q1",
        "A1",
        owner_user_id="teacher-1",
    )
    manager.add_record(
        [teacher_two["id"]],
        "chat",
        "Second",
        "Q2",
        "A2",
        owner_user_id="teacher-2",
    )

    assert [nb["id"] for nb in manager.list_notebooks("teacher-1")] == [teacher_one["id"]]
    assert [nb["id"] for nb in manager.list_notebooks("teacher-2")] == [teacher_two["id"]]
    assert manager.get_notebook(teacher_two["id"], "teacher-1") is None
    assert manager.get_statistics("teacher-1")["total_records"] == 1
    assert manager.get_statistics("teacher-2")["total_records"] == 1
    assert len(manager.list_notebooks(None)) == 2
