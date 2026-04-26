from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

from deeptutor.services.agent_spec.service import AgentSpecService


def _sample_structured() -> dict[str, dict[str, str]]:
    return {
        "identity": {
            "agent_name": "Fraction Coach",
            "subject": "Mathematics",
            "grade_band": "Grade 6",
            "tone": "Warm and direct",
            "primary_language": "Vietnamese",
            "persona_summary": "A teacher-defined tutor for fraction practice.",
        },
        "soul": {
            "teaching_philosophy": "Use evidence before intervention.",
            "when_student_wrong": "Acknowledge the attempt, then diagnose the misconception.",
            "when_student_stuck": "Offer one scaffold at a time.",
            "encouragement_style": "Calm, specific praise.",
        },
        "rules": {
            "do_not_solve_directly": "yes",
            "max_session_minutes": "25",
            "hint_policy": "Give one hint before revealing the next step.",
            "escalation_rule": "Pause and recommend teacher support after repeated confusion.",
            "guardrails": "Never complete the full answer for the student.",
        },
    }


def test_create_pack_writes_markdown_and_versions(tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")

    payload = service.create_pack(
        agent_id="Fraction Coach",
        display_name="Fraction Coach",
        description="Middle-school fraction remediation",
        structured=_sample_structured(),
        files={"CURRICULUM.md": "# Curriculum\n\n- Fractions first.\n"},
    )

    assert payload["agent_id"] == "fraction-coach"
    assert payload["version"] == 1
    assert (tmp_path / "agent_specs" / "fraction-coach" / "IDENTITY.md").exists()
    assert (tmp_path / "agent_specs" / "fraction-coach" / "versions" / "v0001" / "SOUL.md").exists()
    assert "Agent Name: Fraction Coach" in payload["files"]["IDENTITY.md"]
    assert "## Teaching Philosophy" in payload["files"]["SOUL.md"]


def test_save_pack_increments_version_and_preserves_raw_files(tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_sample_structured(),
        files={"CURRICULUM.md": "# Curriculum\n\n- Fractions first.\n"},
    )

    updated = service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach v2",
        description="Updated authoring pack",
        structured={
            **_sample_structured(),
            "identity": {**_sample_structured()["identity"], "tone": "Socratic and encouraging"},
        },
        files={"CURRICULUM.md": "# Curriculum\n\n- Fractions\n- Ratios\n"},
    )

    assert updated["version"] == 2
    assert updated["display_name"] == "Fraction Coach v2"
    assert "Tone: Socratic and encouraging" in updated["files"]["IDENTITY.md"]
    assert updated["files"]["CURRICULUM.md"].startswith("# Curriculum")
    assert (tmp_path / "agent_specs" / "fraction-coach" / "versions" / "v0002" / "CURRICULUM.md").exists()


def test_export_pack_archive_contains_all_markdown_files(tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_sample_structured(),
    )

    blob = service.export_pack_archive("fraction-coach")

    with ZipFile(BytesIO(blob)) as archive:
        names = set(archive.namelist())

    assert "fraction-coach/IDENTITY.md" in names
    assert "fraction-coach/SOUL.md" in names
    assert "fraction-coach/MARKETPLACE.md" in names


def test_get_pack_version_reads_historical_snapshot(tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_sample_structured(),
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion one.\n"},
    )
    service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_sample_structured(),
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion two.\n"},
    )

    version_one = service.get_pack_version("fraction-coach", 1)
    version_two = service.get_pack_version("fraction-coach", 2)

    assert "Version two." not in version_one["files"]["WORKFLOW.md"]
    assert "Version two." in version_two["files"]["WORKFLOW.md"]
    assert version_one["version"] == 1
    assert version_two["version"] == 2
