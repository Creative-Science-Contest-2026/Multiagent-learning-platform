# Task Packet: Realistic Demo Seed Data Expansion

Owner: Codex session
Branch: `fix/demo-realistic-seed-data`
Task ID: `DEMO-SEED-2026-04-30`
Commit tag: `DEMO-SEED`

## Goal

Expand the local demo data reset utility so one explicit command can rebuild a realistic, diverse, demo-safe dataset that fills the teacher-first contest journey end to end: marketplace, imported knowledge packs, assessment review, tutor replay, dashboard evidence, and related intervention traces.

## User-visible outcome

After running the local reset command, the repo should present non-empty, believable data across the main demo screens without requiring manual DB edits or live LLM/API calls.

## Owned files/modules

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/superpowers/tasks/2026-04-30-demo-realistic-seed-data.md`
- `docs/superpowers/specs/2026-04-30-demo-realistic-seed-data-design.md`
- `docs/superpowers/pr-notes/2026-04-30-demo-realistic-seed-data.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if repo-level operating guidance changes

## Do-not-touch files/modules

- `web/`
- `deeptutor/api/`
- `deeptutor/services/` except using existing runtime/storage contracts as-is
- `.env*`
- committed `data/` outputs or any private local data
- lockfiles and dependency manifests

## Design before implementation

### Current behavior

The existing reset utility seeds one demo knowledge pack and two minimal sessions. It is safe and idempotent, but the resulting dataset is too sparse for a realistic full-product video across marketplace, dashboard, review, and tutor replay surfaces.

### Intended behavior change

The reset utility should build a richer local-only dataset using the current file and SQLite persistence layers. The command must remain idempotent and safe, but now create enough metadata, sessions, observations, student states, and teacher-action traces to make the main contest path look realistic and varied.

### Candidate approaches

1. Extend the existing reset utility.
   - Pros: reuses the established safety gate, command entry point, and demo workflow docs; keeps one reset story.
   - Cons: the script becomes denser and needs clearer internal structure.

2. Add a second video-only seed script.
   - Pros: isolates the richer dataset from the original minimal reset flow.
   - Cons: duplicates logic, splits the demo workflow, and increases drift risk.

Chosen approach: extend the existing reset utility with bounded helper functions for each seeded area. This keeps the operator workflow simple and aligned with the current contest runbook.

### Concrete files or modules expected to change

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- lane docs in `docs/superpowers/` plus `ai_first/ACTIVE_ASSIGNMENTS.md` and `ai_first/daily/2026-04-30.md`

### Tests to add or update

- Extend script-level tests for idempotency and safety.
- Add assertions that the seeded DB contains the expected counts and key ids for marketplace/demo sessions/evidence traces.
- Add a focused verification run that the script can be executed repeatedly without duplicate rows.

## Codebase survey

- Entry point: `scripts/contest/reset_demo_data.py`
- Persistence contract: `deeptutor/services/session/sqlite_store.py`
- Dashboard/evidence readers: `deeptutor/api/routers/dashboard.py`
- Existing lane contract baseline: `docs/superpowers/tasks/2026-04-19-scripted-demo-data-reset.md`

## Expected impact surface

Files likely to change:

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/SMOKE_RUNBOOK.md`

Files reviewed but expected to remain unchanged:

- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/api/routers/dashboard.py`
- `web/` screens and API clients

Validation paths that must pass before completion:

- local reset command succeeds against a local API base
- repeated reset command keeps the same dataset shape without duplication
- seeded DB contains believable activity for marketplace, dashboard, assessment review, and tutor replay

## Acceptance criteria

- One explicit local command rebuilds or refreshes the realistic demo dataset.
- Marketplace has diverse shareable pack metadata suitable for search, sort, preview, and import.
- Dashboard has non-empty evidence, diagnoses, recommendations, acknowledgements, feedback, override, action, and intervention traces.
- Assessment review and tutor replay each have multiple believable sessions rather than a single shallow stub.
- The script remains local-only, demo-safe, and idempotent.

