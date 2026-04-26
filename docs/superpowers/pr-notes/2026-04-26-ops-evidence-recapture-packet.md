# PR Note: Dashboard And Agents Evidence Recapture

## Summary

- Adds the dedicated docs-only task packet for recapturing stale contest screenshots after Lane 5 changed the dashboard workflow.
- Recaptures the stale dashboard evidence-first and `/agents` authoring/export screenshots against the current merged UI.
- Updates contest docs so screenshot rows move from `Stale` to `Current` only where fresh artifacts now exist.

## Architecture impact

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was not updated because this PR only creates a docs/evidence execution packet and queue handoff.

```mermaid
flowchart LR
  A["Lane 5 merged dashboard UI"] --> B["Lane 6 marks screenshot rows Stale"]
  B --> C["Recapture packet on docs/evidence branch"]
  C --> D["Fresh dashboard screenshots"]
  C --> E["Fresh /agents screenshots"]
  D --> F["Contest docs move rows to Current"]
  E --> F
```

## Files changed

- `docs/superpowers/tasks/2026-04-26-dashboard-agents-evidence-recapture.md`
- `docs/superpowers/pr-notes/2026-04-26-ops-evidence-recapture-packet.md`
- `docs/contest/screenshots/05-dashboard-evidence-first-overview.png`
- `docs/contest/screenshots/09-dashboard-recent-activity-evidence-first.png`
- `docs/contest/screenshots/10-agents-spec-pack-authoring.png`
- `docs/contest/screenshots/11-agents-spec-pack-export.png`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/README.md`
- `docs/contest/DEMO_SCRIPT.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/daily/2026-04-26.md`

## Validation

- `rg -n "Stale|Current|dashboard|/agents|screenshots|recapture" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check -- ai_first/ACTIVE_ASSIGNMENTS.md ai_first/EXECUTION_QUEUE.md ai_first/daily/2026-04-26.md docs/contest/EVIDENCE_CHECKLIST.md docs/contest/VALIDATION_REPORT.md docs/contest/README.md docs/contest/DEMO_SCRIPT.md docs/contest/SUBMISSION_PACKAGE.md docs/superpowers/tasks/2026-04-26-dashboard-agents-evidence-recapture.md docs/superpowers/pr-notes/2026-04-26-ops-evidence-recapture-packet.md`
