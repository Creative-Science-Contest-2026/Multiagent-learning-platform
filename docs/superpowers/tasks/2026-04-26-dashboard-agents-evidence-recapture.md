# Feature Pod Task: Dashboard And Agents Evidence Recapture

Task ID: `OPS_EVIDENCE_RECAPTURE_DASHBOARD_AGENTS`
Commit tag: `OPS-EVIDENCE`
Owner: Session-specific
Branch: `docs/evidence-dashboard-agents-recapture`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Recapture the contest screenshot evidence that became stale after the evidence-first dashboard workflow merged and while the hybrid `/agents` authoring proof still lacks browser-backed artifacts.

## User-visible outcome

- Contest docs can truthfully mark dashboard and `/agents` screenshot rows as `Current`.
- Reviewers see the current teacher workflow instead of the pre-Lane-5 dashboard layout.
- Hybrid proof remains calibrated because screenshots match the actual merged UI.

## Owned files/modules

- `docs/contest/screenshots/*`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/DEMO_SCRIPT.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-26-dashboard-agents-evidence-recapture.md`
- `docs/superpowers/pr-notes/*`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/daily/2026-04-26.md`

## Do-not-touch files/modules

- `deeptutor/services/`
- `deeptutor/api/routers/`
- `web/app/`
- `web/components/`
- `ai_first/AI_OPERATING_PROMPT.md` unless the recapture workflow itself changes operating rules

## Evidence contract

- Reuse the latest smoke-backed validation from PR `#145` unless a new smoke run is required for browser capture confidence.
- Recapture only the stale rows:
  - dashboard evidence-first teacher workflow overview
  - dashboard recent activity below the new workflow
  - `/agents` structured authoring view
  - `/agents` export action view
- Only move `Stale` -> `Current` after new screenshots are produced, linked, and visually checked.

## Acceptance criteria

- Every stale dashboard or `/agents` screenshot row has a fresh artifact in `docs/contest/screenshots/`.
- Contest evidence docs reference the new capture date and source lane.
- Hybrid `/agents` claims remain bounded to authoring/export proof unless live runtime binding is freshly verified.
- This lane does not change product/runtime code.

## Required tests

- `rg -n "Stale|Current|dashboard|/agents|screenshots" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Open each new screenshot and confirm it matches the current merged UI.
- Confirm no private data or credentials appear in the captures.
- Confirm dashboard screenshots show the evidence-first workflow from Lane 5.
- Confirm `/agents` screenshots show structured authoring and export without overclaiming runtime binding.

## Parallel-work notes

- This lane is docs/evidence-only and browser-heavy.
- If browser capture is unavailable, leave rows `Stale` and document the blocker explicitly instead of inventing artifacts.
- Do not “fix” UI or backend issues from this lane; capture the current merged behavior only.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.

## Handoff notes

- Lane 5 (`#144`) changed the dashboard hierarchy, so the previous `05-dashboard-summary-and-activity.png` is no longer sufficient evidence for the current teacher workflow.
- Lane 6 (`#145`) already updated contest docs to mark dashboard and `/agents` rows `Stale`.
- The next worker should start from `origin/main`, use demo-safe data, and only mark screenshot rows `Current` after browser-backed recapture.
