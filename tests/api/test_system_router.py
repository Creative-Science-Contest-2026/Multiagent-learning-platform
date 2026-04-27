from __future__ import annotations

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover - optional dependency in lightweight envs
    FastAPI = None
    TestClient = None

from deeptutor.services.session.sqlite_store import SQLiteSessionStore

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(store: SQLiteSessionStore, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import system

    app = FastAPI()
    app.include_router(system.router, prefix="/api/v1/system")
    monkeypatch.setattr(system, "get_sqlite_session_store", lambda: store)
    return app


def test_system_pilot_feedback_status_stays_explicit_when_empty(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    with TestClient(_build_app(store, monkeypatch)) as client:
        response = client.get("/api/v1/system/pilot-feedback-status")

    assert response.status_code == 200
    assert response.json() == {
        "status": "no_pilot_evidence_yet",
        "record_count": 0,
        "levels_present": [],
        "latest_feedback_date": None,
        "items": [],
    }


def test_system_pilot_feedback_create_and_list_round_trip(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = SQLiteSessionStore(tmp_path / "chat_history.db")

    with TestClient(_build_app(store, monkeypatch)) as client:
        create_response = client.post(
            "/api/v1/system/pilot-feedback",
            json={
                "evidence_level": "limited_external_feedback",
                "source_label": "Teacher review meeting",
                "participant_role": "teacher",
                "feedback_date": "2026-04-28",
                "scope_note": "two-teacher demo review",
                "finding_summary": "Reviewers understood the flow and asked for clearer classroom boundary notes.",
                "recommendation_note": "Preserve the no-pilot-yet wording until broader external use exists.",
                "artifact_ref": "docs/contest/PILOT_STATUS.md",
                "verified_by": "submission-team",
            },
        )
        list_response = client.get("/api/v1/system/pilot-feedback")
        status_response = client.get("/api/v1/system/pilot-feedback-status")

    assert create_response.status_code == 200
    created = create_response.json()
    assert created["evidence_level"] == "limited_external_feedback"
    assert created["verified_by"] == "submission-team"

    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["source_label"] == "Teacher review meeting"

    assert status_response.status_code == 200
    assert status_response.json()["status"] == "feedback_records_available"
    assert status_response.json()["record_count"] == 1
    assert status_response.json()["levels_present"] == ["limited_external_feedback"]
