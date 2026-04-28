# Feature Pod Task: Three-Session Submission Close Master Coordination

Task ID: `OPS_SUBMISSION_CLOSE_MASTER`
Commit tag: `OPS-SUBMIT`
Owner: Coordination lane
Branch: `docs/submission-close-master`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Turn the approved three-session submission-close design into one execution contract that three parallel AI sessions can follow without colliding on the same files or rediscovering submission context.

## User-visible outcome

- Three session packets exist with explicit owned files.
- Phase 1 and Phase 2 are separated.
- Session startup order and merge order are explicit.
- The submission-close path is discoverable from one coordination document.

## Owned files/modules

- `docs/superpowers/specs/2026-04-28-three-session-submission-close-design.md`
- `docs/superpowers/plans/2026-04-28-three-session-submission-close.md`
- `docs/superpowers/tasks/2026-04-28-submission-close-master-coordination.md`
- `docs/superpowers/tasks/2026-04-28-session-a-submission-scope-and-narrative.md`
- `docs/superpowers/tasks/2026-04-28-session-b-validation-and-evidence.md`
- `docs/superpowers/tasks/2026-04-28-session-c-runtime-fix-and-polish.md`
- `docs/superpowers/pr-notes/three-session-submission-close-plan.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-28.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `web/next-env.d.ts`
- `.env*`
- committed `data/` files

## Session startup order

1. Session A starts first on scope and narrative.
2. Session B starts in parallel on validation and evidence.
3. Session C starts only in standby analysis mode until Session B reports a blocker fix or the human explicitly opens Phase 2 polish.

## Merge order

1. Coordination packet PR
2. Session A and Session B PRs in parallel
3. Any narrow Session C fix PRs
4. Session A or Session B closure PRs
5. Optional Phase 2 Session C polish PRs

## PR train mapping

### Phase 1

- `PR-CLOSE-01` -> Session A
- `PR-CLOSE-02` -> Session A
- `PR-CLOSE-03` -> Session B
- `PR-CLOSE-04` -> Session B
- `PR-CLOSE-05` -> Session B
- `PR-CLOSE-06` -> Session A
- `PR-CLOSE-07` -> Session A
- `PR-CLOSE-08` -> Session A
- `PR-CLOSE-09` -> Session A after Session B outputs are merged

### Phase 2

- `PR-POLISH-01` -> Session C
- `PR-POLISH-02` -> Session C
- `PR-POLISH-03` -> Session C
- `PR-POLISH-04` -> Session A or Session C depending on whether the change is doc-only or product-facing
- `PR-POLISH-05` -> Session B

## Conflict-minimizing rules

1. `docs/contest/README.md` is Session A territory.
2. `docs/contest/VALIDATION_REPORT.md`, `SMOKE_RUNBOOK.md`, `DEMO_DATA_RESET.md`, and `EVIDENCE_CHECKLIST.md` are Session B territory.
3. Product-facing runtime or UI files are Session C territory only when a proven blocker or approved polish target exists.
4. Split mixed narrative-plus-validation work into separate PRs instead of forcing shared ownership.

## Execution note

This packet is the coordination entrypoint only. The actual work starts from the three session packets linked below:

- `docs/superpowers/tasks/2026-04-28-session-a-submission-scope-and-narrative.md`
- `docs/superpowers/tasks/2026-04-28-session-b-validation-and-evidence.md`
- `docs/superpowers/tasks/2026-04-28-session-c-runtime-fix-and-polish.md`
