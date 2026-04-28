# Feature Pod Task: Session C Runtime Fix And Optional Polish

Task ID: `OPS_SUBMISSION_CLOSE_C`
Commit tag: `OPS-C`
Owner: Session C
Branch: `fix/submission-close-session-c`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Absorb any narrow runtime blocker found during validation and, only after Phase 1 is safe, execute optional Phase 2 polish with minimal impact on the submission package.

## User-visible outcome

- Real contest blockers can be fixed without cross-lane file collisions.
- Optional polish work is isolated from the submission-closing docs lanes.

## Owned files/modules

- contest-facing `web/app/` screens directly involved in the core loop
- contest-facing `web/components/` surfaces directly involved in the core loop
- any narrow `deeptutor/` runtime file required to fix a proven contest blocker
- `docs/superpowers/tasks/2026-04-28-session-c-runtime-fix-and-polish.md`

## Do-not-touch files/modules

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/competition/`
- `docs/contest/SUBMISSION_PACKAGE.md`

## Trigger conditions

Session C should only move from standby into active implementation when at least one of these is true:

1. Session B reports a concrete blocker in the contest loop that requires a product fix.
2. Phase 1 is effectively complete and the human explicitly approves Phase 2 polish.

## PR ownership

- narrow fix PRs derived from `PR-CLOSE-03`
- `PR-POLISH-01 Teacher-First Entry Polish`
- `PR-POLISH-02 Core Loop Visibility Polish`
- `PR-POLISH-03 Differentiation Wording Sweep`
- product-facing portions of `PR-POLISH-04 Judge-Facing Visual Asset Polish`

## Output contract

- Do not create new submission claims.
- Do not rewrite Phase 1 docs from this lane.
- Keep fixes surgical and traceable back to Session B validation findings.
