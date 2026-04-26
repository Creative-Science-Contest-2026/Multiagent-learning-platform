# Feature Pod Task: Lane 3 Observation and Student State

Owner: Session-specific
Branch: `pod-a/observation-student-state`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Extend the merged Wave 1 evidence spine so observation capture and student-state updates become broader, cleaner, and more reusable.

## User-visible outcome

- Student evidence is captured consistently across assessment and tutoring flows.
- Student state becomes richer without blending facts and inference.
- Downstream diagnosis and teacher insight features receive better evidence quality.

## Owned files/modules

- `deeptutor/services/evidence/extractor.py`
- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/services/session/context_builder.py`
- `deeptutor/services/session/turn_runtime.py`
- `tests/services/evidence/test_extractor.py`
- `tests/services/session/test_sqlite_store.py`
- `tests/core/test_capabilities_runtime.py`
- `docs/superpowers/tasks/2026-04-26-lane-3-observation-student-state.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/evidence/diagnosis.py`
- `deeptutor/services/evidence/teacher_insights.py`
- `deeptutor/api/routers/dashboard.py`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/`

## API/data contract

- `Observed` must remain separate from `Inferred`.
- Add tutoring-compatible observation capture without rewriting diagnosis rules.
- Student-state summaries may evolve, but raw evidence must remain inspectable and reversible.

## Acceptance criteria

- Observation schema supports both assessment and tutoring inputs.
- Student-state rollups include repeated mistakes, support level, confidence trend, and recency-aware summaries.
- Raw observations remain queryable without depending on diagnosis output.
- Existing Wave 1 evidence spine behavior does not regress.

## Required tests

- Evidence extractor tests
- Session store persistence tests
- Any required runtime tests for tutoring observation capture
- `git diff --check`

## Manual verification

- Run one quiz session and one tutor session for the same learner.
- Verify new observations appear in storage without corrupting old rows.
- Verify student-state summaries update while preserving raw evidence trace.

## Parallel-work notes

- Start from merged `main`; do not reimplement Wave 1 from scratch.
- This lane may strengthen observation quality, but must not silently change diagnosis semantics owned by Lane 4.
- If evidence fields need a cross-lane rename, stop and ask the human before proceeding.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if the evidence layer contract or storage model changes materially.

## Handoff notes

- This is Session = Lane 3.
- Treat `main` after PR `#132` as the baseline.
- Hand off richer observation/state fields to Lane 4 and Lane 5 through explicit documented contracts.
