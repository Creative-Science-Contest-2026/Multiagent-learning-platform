from __future__ import annotations

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None
    TestClient = None

from deeptutor.services.agent_spec.service import AgentSpecService

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(service: AgentSpecService, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import agent_specs

    app = FastAPI()
    app.include_router(agent_specs.router, prefix="/api/v1/agent-specs")
    monkeypatch.setattr(agent_specs, "get_agent_spec_service", lambda: service)
    return app


def _payload(agent_id: str = "fraction-coach") -> dict:
    return {
        "agent_id": agent_id,
        "display_name": "Fraction Coach",
        "description": "Teacher-authored fraction tutor",
        "structured": {
            "identity": {
                "agent_name": "Fraction Coach",
                "subject": "Mathematics",
                "grade_band": "Grade 6",
                "tone": "Warm and direct",
                "primary_language": "Vietnamese",
                "persona_summary": "A tutor for fraction remediation.",
            },
            "soul": {
                "teaching_philosophy": "Use evidence first.",
                "when_student_wrong": "Diagnose before correcting.",
                "when_student_stuck": "Use a single scaffold.",
                "encouragement_style": "Specific and calm.",
            },
            "rules": {
                "do_not_solve_directly": "yes",
                "max_session_minutes": "25",
                "hint_policy": "One hint at a time.",
                "escalation_rule": "Escalate after repeated confusion.",
                "guardrails": "Never finish the full answer.",
            },
        },
        "files": {
            "CURRICULUM.md": "# Curriculum\n\n- Fractions first.\n",
        },
    }


def test_agent_specs_router_supports_create_list_update_and_export(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")

    with TestClient(_build_app(service, monkeypatch)) as client:
        created = client.post("/api/v1/agent-specs", json=_payload())
        assert created.status_code == 200
        assert created.json()["agent_id"] == "fraction-coach"

        listing = client.get("/api/v1/agent-specs")
        assert listing.status_code == 200
        assert listing.json()["items"][0]["agent_id"] == "fraction-coach"

        detail = client.get("/api/v1/agent-specs/fraction-coach")
        assert detail.status_code == 200
        assert detail.json()["structured"]["identity"]["subject"] == "Mathematics"

        payload = _payload()
        payload["display_name"] = "Fraction Coach Revised"
        payload["files"]["WORKFLOW.md"] = "# Workflow\n\n1. Teach\n2. Practice\n"
        updated = client.put("/api/v1/agent-specs/fraction-coach", json=payload)
        assert updated.status_code == 200
        assert updated.json()["version"] == 2

        exported = client.get("/api/v1/agent-specs/fraction-coach/export")
        assert exported.status_code == 200
        assert exported.headers["content-type"] == "application/zip"


def test_agent_specs_router_returns_404_for_missing_pack(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")

    with TestClient(_build_app(service, monkeypatch)) as client:
        response = client.get("/api/v1/agent-specs/missing-pack")

    assert response.status_code == 404
