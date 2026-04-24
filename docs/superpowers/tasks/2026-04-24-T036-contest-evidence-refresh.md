# Feature Pod Task: Contest Smoke and Evidence Refresh

Owner: Codex
Branch: `docs/t036-contest-evidence-refresh`
GitHub Issue: `#95`

## Goal

Refresh the contest smoke-backed validation record against current `main`, update evidence freshness honestly, and repair any control-plane drift uncovered during the refresh.

## User-visible outcome

- Contest validation docs reflect a real 2026-04-24 smoke run instead of the older 2026-04-19 record.
- Command evidence is marked `Current` based on the new smoke run.
- Screenshot evidence is marked `Stale` until a human recapture happens after the recent UI merges.

## Owned files/modules

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SMOKE_RUNBOOK.md` only if the executed smoke path needs clarification
- `docs/superpowers/tasks/2026-04-24-T036-contest-evidence-refresh.md`
- `docs/superpowers/pr-notes/2026-04-24-t036-contest-evidence-refresh.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Product/runtime source files unless the smoke lane finds a real blocker that must be fixed first
- Screenshot image assets themselves
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the lane unexpectedly changes product/runtime architecture
- Root license and upstream attribution files

## Evidence contract

- Use the scripted local reset command before the smoke pass:
  - `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`
- Use the existing local backend startup path:
  - `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m deeptutor_cli.main serve --host 127.0.0.1 --port 8001`
- Verify:
  - `curl -s http://127.0.0.1:8001/api/v1/system/status`
  - `curl -s http://127.0.0.1:8001/api/v1/knowledge/list`
  - `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview`
  - `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent`
  - `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo`
  - `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo`
  - `cd web && npm run build`

## Acceptance criteria

- Validation docs cite the 2026-04-24 smoke-backed pass with concrete commands and outcomes.
- Any stale screenshot state is called out explicitly instead of left as `Current`.
- AI-first task tracking shows `T036` as the active short task on this branch.
- No product/runtime scope is broadened beyond the evidence refresh lane.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "2026-04-24|Current|Stale|Blocked|contest-demo-quadratics|contest-assessment-demo|contest-tutor-demo" docs/contest ai_first`
- `git diff --check`

## Manual verification

- Confirm the reset script recreates `contest-demo-quadratics`, `contest-assessment-demo`, and `contest-tutor-demo`.
- Confirm backend endpoints return the expected demo-safe metadata and recent activity.
- Confirm the frontend production build passes from the fresh worktree after dependency install.

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T035` merged to `main` through PR `#93`, and docs-only sync merged through PR `#94`.
- The strict-order feature queue was empty before deriving this short task.
- Treat screenshot freshness conservatively: if no new capture happened, mark it `Stale`.
