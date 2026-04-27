from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def build_check_plan(api_base: str, include_frontend: bool) -> list[dict]:
    plan = [
        {
            "name": "demo_reset",
            "command": f"python3 -m scripts.contest.reset_demo_data --project-root . --api-base {api_base}",
            "manual_followup_required": False,
        },
        {
            "name": "system_status",
            "command": f"curl -s {api_base}/api/v1/system/status",
            "manual_followup_required": False,
        },
        {
            "name": "knowledge_list",
            "command": f"curl -s {api_base}/api/v1/knowledge/list",
            "manual_followup_required": False,
        },
        {
            "name": "dashboard_overview",
            "command": f"curl -s {api_base}/api/v1/dashboard/overview",
            "manual_followup_required": False,
        },
        {
            "name": "dashboard_recent",
            "command": f"curl -s {api_base}/api/v1/dashboard/recent",
            "manual_followup_required": False,
        },
        {
            "name": "assessment_session",
            "command": f"curl -s {api_base}/api/v1/sessions/contest-assessment-demo",
            "manual_followup_required": False,
        },
        {
            "name": "tutor_session",
            "command": f"curl -s {api_base}/api/v1/sessions/contest-tutor-demo",
            "manual_followup_required": False,
        },
    ]
    if include_frontend:
        plan.append(
            {
                "name": "frontend_build",
                "command": "cd web && npm ci && npm run build",
                "manual_followup_required": False,
            }
        )
    return plan


def build_status_artifact(project_root: str, api_base: str, checks: list[dict]) -> dict:
    normalized_checks = []
    for check in checks:
        normalized_checks.append(
            {
                "name": check["name"],
                "command": check["command"],
                "status": check["status"],
                "summary": check["summary"],
                "manual_followup_required": check.get("manual_followup_required", False),
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": project_root,
        "api_base": api_base,
        "proof_level": "validated_prototype",
        "checks": normalized_checks,
        "manual_artifacts": {
            "screenshots": "manual",
            "video": "manual",
        },
    }


def run_check(command: str, cwd: Path) -> dict:
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    summary = result.stdout.strip() or result.stderr.strip() or "no output"
    return {
        "status": "passed" if result.returncode == 0 else "failed",
        "summary": summary[:500],
    }


def write_artifact(project_root: Path, artifact: dict) -> Path:
    target = project_root / "ai_first" / "evidence" / "evidence_status.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh command-backed contest evidence status.")
    parser.add_argument("--project-root", default=".", help="Repository root.")
    parser.add_argument("--api-base", default="http://localhost:8001", help="Local API base.")
    parser.add_argument("--include-frontend", action="store_true", help="Include frontend build validation.")
    parser.add_argument(
        "--skip-execution",
        action="store_true",
        help="Only emit the current artifact shape without running commands.",
    )
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    plan = build_check_plan(api_base=args.api_base, include_frontend=args.include_frontend)

    checks = []
    for item in plan:
        if args.skip_execution:
            checks.append(
                {
                    "name": item["name"],
                    "command": item["command"],
                    "status": "planned",
                    "summary": "execution skipped",
                    "manual_followup_required": item["manual_followup_required"],
                }
            )
            continue
        outcome = run_check(item["command"], root)
        checks.append(
            {
                "name": item["name"],
                "command": item["command"],
                "status": outcome["status"],
                "summary": outcome["summary"],
                "manual_followup_required": item["manual_followup_required"],
            }
        )

    artifact = build_status_artifact(
        project_root=str(root),
        api_base=args.api_base,
        checks=checks,
    )
    path = write_artifact(root, artifact)
    print(json.dumps({"artifact_path": str(path), "checks": len(checks)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
