# Task Packet: Demo Seed Vietnamese Refresh

Owner: Codex session
Branch: `fix/demo-seed-vietnamese-refresh`
Task ID: `DEMO-SEED-VI-2026-05-01`
Commit tag: `DEMO-SEED-VI`

## Goal

Refresh the local contest demo seed so visible mock content is Vietnamese and student-facing, while making the script's cleanup-before-reseed behavior explicit enough that repeated runs cannot be mistaken for duplicate accumulation.

## Owned files/modules

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/superpowers/tasks/2026-05-01-demo-seed-vietnamese-refresh.md`
- `docs/superpowers/specs/2026-05-01-demo-seed-vietnamese-refresh-design.md`
- `docs/superpowers/pr-notes/2026-05-01-demo-seed-vietnamese-refresh.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-05-01.md`

## Do-not-touch files/modules

- `web/`
- `deeptutor/api/`
- `deeptutor/services/` runtime modules beyond consuming their existing contracts
- lockfiles
- `.env*`
- committed generated `data/`

## Design before implementation

### Current behavior

The richer demo seed already clears demo-owned rows before reseeding, but much of the seeded visible content is still English or English-leaning. The cleanup behavior is implicit in the implementation and not clearly surfaced to the operator.

### Intended behavior change

The seed should keep the same dataset shape and idempotency, but:

- visible metadata, exercise content, and tutor transcript content should read naturally in Vietnamese for Vietnamese teachers and students;
- the reset command/result and runbook should state clearly that old demo data is cleared before the new mock dataset is written.

### Candidate approaches

1. Translate only the highest-visibility strings and add one explicit cleanup note.
   - Pros: smallest safe change, preserves dataset structure and tests.
   - Cons: some lower-visibility English could remain.

2. Translate every teacher/student-facing seeded string and expose cleanup in both code output and docs.
   - Pros: aligns best with the user's video/demo goal.
   - Cons: wider seed-data text diff.

Chosen approach: 2. Keep the data shape unchanged, but fully localize visible seed content and surface cleanup explicitly in the result payload plus runbook wording.

### Codebase survey

- Entry point: `scripts/contest/reset_demo_data.py`
- Existing contract tests: `tests/scripts/test_reset_demo_data.py`
- Operator doc: `docs/contest/DEMO_DATA_RESET.md`

### Expected impact surface

Files likely to change:

- `scripts/contest/reset_demo_data.py`
- `tests/scripts/test_reset_demo_data.py`
- `docs/contest/DEMO_DATA_RESET.md`

Files reviewed but expected to remain unchanged:

- `docs/contest/SMOKE_RUNBOOK.md`
- `deeptutor/services/*`

### Tests to add or update

- assert seeded anchor metadata is Vietnamese
- assert at least one seeded assessment or tutor content sample is Vietnamese
- assert the reset result explicitly reports cleanup-before-reseed

