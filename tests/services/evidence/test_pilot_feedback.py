from __future__ import annotations

from deeptutor.services.session.sqlite_store import SQLiteSessionStore

from deeptutor.services.evidence.pilot_feedback import (
    build_pilot_feedback_status,
    create_pilot_feedback,
    list_pilot_feedback,
)


def test_pilot_feedback_status_defaults_to_no_pilot_evidence(tmp_path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    status = build_pilot_feedback_status(store)

    assert status == {
        "status": "no_pilot_evidence_yet",
        "record_count": 0,
        "levels_present": [],
        "latest_feedback_date": None,
        "items": [],
    }


def test_pilot_feedback_records_round_trip_with_claim_safe_metadata(tmp_path) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    record = create_pilot_feedback(
        store,
        evidence_level="walkthrough",
        source_label="Teacher walkthrough",
        participant_role="teacher",
        feedback_date="2026-04-28",
        scope_note="single-teacher structured walkthrough",
        finding_summary="The MVP flow is clear, but the evidence boundary should stay explicit.",
        recommendation_note="Add a clearer note about evidence freshness before a wider demo.",
        artifact_ref="docs/contest/PILOT_STATUS.md",
        verified_by="internal-review",
    )

    listed = list_pilot_feedback(store)
    status = build_pilot_feedback_status(store)

    assert record["evidence_level"] == "walkthrough"
    assert listed[0]["source_label"] == "Teacher walkthrough"
    assert listed[0]["artifact_ref"] == "docs/contest/PILOT_STATUS.md"
    assert status["status"] == "feedback_records_available"
    assert status["record_count"] == 1
    assert status["levels_present"] == ["walkthrough"]
    assert status["latest_feedback_date"] == "2026-04-28"

