from __future__ import annotations

import pytest

try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    FastAPI = None
    TestClient = None

from deeptutor.services.agent_spec.service import AgentSpecService
from deeptutor.services.runtime_policy import compiler as runtime_policy_compiler

pytestmark = pytest.mark.skipif(FastAPI is None or TestClient is None, reason="fastapi not installed")


def _build_app(service: AgentSpecService, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    from deeptutor.api.routers import agent_specs

    app = FastAPI()
    app.include_router(agent_specs.router, prefix="/api/v1/agent-specs")
    monkeypatch.setattr(agent_specs, "get_agent_spec_service", lambda: service)
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)
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


def test_agent_specs_router_returns_runtime_policy_audit_for_latest_and_versioned_pack(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_payload()["structured"],
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion one.\n"},
    )
    service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            **_payload()["structured"],
            "soul": {
                **_payload()["structured"]["soul"],
                "teaching_philosophy": "Version two philosophy.",
            },
        },
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion two.\n"},
    )

    with TestClient(_build_app(service, monkeypatch)) as client:
        latest = client.get("/api/v1/agent-specs/fraction-coach/runtime-policy-audit")
        assert latest.status_code == 200
        assert latest.json()["agent_spec_version"] == 2
        assert "Version two philosophy." in latest.json()["runtime_policy"]["slices"]["SOUL"]

        version_one = client.get("/api/v1/agent-specs/fraction-coach/runtime-policy-audit?version=1")
        assert version_one.status_code == 200
        assert version_one.json()["agent_spec_version"] == 1
        assert "Version two philosophy." not in version_one.json()["runtime_policy"]["slices"]["SOUL"]


def test_agent_specs_router_returns_404_for_missing_runtime_policy_audit_pack_or_version(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured=_payload()["structured"],
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion one.\n"},
    )

    with TestClient(_build_app(service, monkeypatch)) as client:
        missing_pack = client.get("/api/v1/agent-specs/missing-pack/runtime-policy-audit")
        missing_version = client.get("/api/v1/agent-specs/fraction-coach/runtime-policy-audit?version=9")

    assert missing_pack.status_code == 404
    assert missing_version.status_code == 404
