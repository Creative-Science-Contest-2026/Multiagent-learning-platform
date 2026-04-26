# Feature Pod Task: Lane 4 Diagnosis and Recommendation Engine

Task ID: `L4_DIAGNOSIS_RECOMMENDATION`
Commit tag: `L4`
Owner: Session-specific
Branch: `pod-a/diagnosis-recommendation`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Evolve the merged Wave 1 diagnosis backbone into a stronger hybrid recommendation engine with clearer hypothesis taxonomy, confidence, and action mapping.

## User-visible outcome

- Teacher recommendations become more explicit, evidence-backed, and useful.
- Small-group recommendations become less ad hoc and more consistent.
- Diagnosis remains auditable rather than collapsing into free-form LLM claims.

## Owned files/modules

- `deeptutor/services/evidence/diagnosis.py`
- `deeptutor/services/evidence/teacher_insights.py`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/dashboard.py`
- `tests/services/evidence/test_diagnosis.py`
- `tests/api/test_assessment_router.py`
- `tests/api/test_dashboard_router.py`
- `docs/superpowers/tasks/2026-04-26-lane-4-diagnosis-recommendation.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/services/session/turn_runtime.py`
- `deeptutor/services/prompt/`
- `web/app/(workspace)/dashboard/`
- `web/components/dashboard/TeacherInsightPanel.tsx`

## API/data contract

- `Inferred` must remain derived from observed evidence, never the other way around.
- Confidence tags are engine-owned, not LLM-owned.
- Recommended actions should map to explicit action types before any narrative explanation.

## Acceptance criteria

- Diagnosis taxonomy expands cleanly beyond the Wave 1 placeholder behavior.
- Per-student and small-group actions are ranked deterministically before narrative wording is added.
- The engine can abstain when evidence is weak or contradictory.
- The lane does not rewrite storage schema or UI ownership without agreement.

## Required tests

- Diagnosis engine tests for taxonomy, confidence, and abstain behavior
- Router tests for assessment diagnosis and teacher insight payloads
- `git diff --check`

## Manual verification

- Seed at least two misconception patterns and confirm the engine distinguishes them.
- Verify confidence tags track evidence density rather than arbitrary heuristics.
- Verify small-group recommendations only appear when grouping criteria are met.

## Parallel-work notes

- Start from the merged Wave 1 spine on `main`.
- This lane owns recommendation logic, not the raw observation capture contract.
- If a change requires new observed fields, ask the human or coordinate through a documented Lane 3 contract update.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if diagnosis/recommendation pathways change materially.

## Handoff notes

- This is Session = Lane 4.
- Coordinate with Lane 5 only through response payloads, not shared UI assumptions.
- Coordinate with Lane 6 through explicit evaluation cases and demo scenarios.
