from scripts.contest.refresh_evidence_status import (
    build_check_plan,
    build_status_artifact,
)


def test_build_check_plan_contains_expected_core_checks():
    plan = build_check_plan(api_base="http://localhost:8001", include_frontend=False)
    names = [item["name"] for item in plan]
    assert names == [
        "demo_reset",
        "system_status",
        "knowledge_list",
        "dashboard_overview",
        "dashboard_recent",
        "assessment_session",
        "tutor_session",
    ]


def test_build_status_artifact_marks_manual_followups():
    checks = [
        {
            "name": "system_status",
            "command": "curl -s http://localhost:8001/api/v1/system/status",
            "status": "passed",
            "summary": "ok",
        },
    ]
    artifact = build_status_artifact(
        project_root=".",
        api_base="http://localhost:8001",
        checks=checks,
    )
    assert artifact["checks"][0]["manual_followup_required"] is False
    assert artifact["manual_artifacts"]["screenshots"] == "manual"
    assert artifact["manual_artifacts"]["video"] == "manual"
