# Task Packet: F123 Casepack And Evaluation Dataset Expansion

- Task ID: `F123_CASEPACK_AND_EVALUATION_DATASET_EXPANSION`
- Commit tag: `F123`
- Owner: `Codex`
- Status: `brainstorming`

## Objective

Grow the current judge-safe case studies into a reusable validation casepack that is machine-readable, contest-safe, and ready for later automation without widening runtime product scope.

## Owned Files

- `ai_first/evidence/`
- `docs/contest/`
- `tests/` only for bounded casepack validation
- `docs/superpowers/tasks/2026-04-28-f123-casepack-and-evaluation-dataset-expansion.md`
- `docs/superpowers/specs/2026-04-28-f123-casepack-and-evaluation-dataset-expansion-design.md`
- `docs/superpowers/plans/2026-04-28-f123-casepack-and-evaluation-dataset-expansion.md`
- `docs/superpowers/pr-notes/2026-04-28-f123-casepack-and-evaluation-dataset-expansion.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`

## Do-Not-Touch

- runtime product code outside a bounded validation helper if one becomes strictly necessary
- dashboard UX
- assessment generation flow
- session runtime / agent-spec plumbing
- control-plane files outside those listed above

## Acceptance Criteria

1. A machine-readable casepack exists under `ai_first/evidence/` as source-of-truth for reusable validation scenarios.
2. The casepack expands beyond the current diagnosis prose into multiple judge-safe scenario types.
3. Contest-facing docs explain how to read and use the casepack without overclaiming model accuracy.
4. A bounded validation check prevents schema drift or missing required fields.
5. AI-first tracking is updated with scope, status, validation, and handoff notes.

## Validation

- `python -m json.tool` or equivalent schema/format validation for the casepack
- targeted validation test if one is added
- `git diff --check`
