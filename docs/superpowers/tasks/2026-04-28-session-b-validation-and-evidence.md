# Feature Pod Task: Session B Validation And Evidence

Task ID: `OPS_SUBMISSION_CLOSE_B`
Commit tag: `OPS-B`
Owner: Session B
Branch: `docs/submission-close-session-b`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Validate the current contest loop on `main`, refresh the demo-data and smoke contract, and keep all evidence status honest and current.

## User-visible outcome

- The team knows which contest claims are currently proven.
- Evidence artifacts are marked current, pending, optional, or blocked.
- Validation failures become explicit blockers rather than silent doc drift.

## Owned files/modules

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/evidence/demo-script.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/evidence/evidence_status.json`
- `docs/superpowers/tasks/2026-04-28-session-b-validation-and-evidence.md`

## Do-not-touch files/modules

- `ai_first/competition/product-description.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `deeptutor/`
- `web/`

## PR ownership

- `PR-CLOSE-03 Core Loop Runtime Revalidation`
- `PR-CLOSE-04 Demo Data and Smoke Contract Refresh`
- `PR-CLOSE-05 Evidence Bundle Refresh`
- `PR-POLISH-05 Post-Polish Evidence Recapture`

## Blocker escalation rule

- If the contest loop fails in a way that breaks `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`, stop the docs-only lane and request a narrow Session C fix PR.
- Do not patch runtime behavior from Session B.
- Do not soften wording to hide a failing proof point.

## Output contract

- Validation wording must align to Session A's claim contract once it is frozen.
- Evidence freshness status must reflect actual smoke-backed behavior, not aspirational cleanup.
