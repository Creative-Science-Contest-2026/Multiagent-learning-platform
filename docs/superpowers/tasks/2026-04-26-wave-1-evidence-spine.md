# Feature Pod Task: Wave 1 Evidence Spine

Owner: Codex
Branch: `pod-a/wave1-evidence-spine`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Implement the first end-to-end `Observed -> Inferred -> Recommended Action` spine on top of the current assessment, session, and dashboard stack.

## User-visible outcome

- Assessment sessions produce structured observations and student-state summaries.
- Teachers can view per-student diagnosis and small-group recommendations from the dashboard.
- The assessment API exposes a structured diagnosis payload instead of only a topic recommendation.

## Owned files/modules

- `deeptutor/services/evidence/__init__.py`
- `deeptutor/services/evidence/contracts.py`
- `deeptutor/services/evidence/extractor.py`
- `deeptutor/services/evidence/diagnosis.py`
- `deeptutor/services/evidence/teacher_insights.py`
- `deeptutor/services/session/sqlite_store.py`
- `deeptutor/services/session/__init__.py`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/dashboard.py`
- `tests/services/evidence/test_extractor.py`
- `tests/services/evidence/test_diagnosis.py`
- `tests/services/session/test_sqlite_store.py`
- `tests/api/test_assessment_router.py`
- `tests/api/test_dashboard_router.py`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/lib/dashboard-api.ts`
- `web/app/(workspace)/dashboard/page.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-26.md`
- `docs/superpowers/pr-notes/2026-04-26-wave-1-evidence-spine.md`

## Do-not-touch files/modules

- `docs/superpowers/specs/2026-04-26-contest-mvp-hybrid-lanes-design.md`
- `docs/superpowers/plans/2026-04-26-contest-mvp-spine-implementation.md`
- `web/app/(utility)/knowledge/`
- `deeptutor/services/prompt/`
- `deeptutor/knowledge/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`

## API/data contract

- Add normalized observation persistence in SQLite without changing existing session/message tables.
- Add `GET /api/v1/assessment/diagnosis/{session_id}` returning structured observation, diagnosis, and recommendation data.
- Change `GET /api/v1/dashboard/insights` to return structured `students` and `small_groups` payloads for the teacher dashboard.

## Acceptance criteria

- New evidence service layer exists and is covered by focused tests.
- SQLite store can persist and read observations plus student-state summaries.
- Assessment diagnosis endpoint returns structured diagnosis for seeded assessment sessions.
- Dashboard insights endpoint aggregates per-student and small-group recommendation payloads.
- Teacher dashboard renders the structured insight payload without lint errors.

## Required tests

- `pytest tests/services/evidence/test_extractor.py tests/services/evidence/test_diagnosis.py tests/services/session/test_sqlite_store.py tests/api/test_assessment_router.py tests/api/test_dashboard_router.py -v`
- `cd web && npm run lint`
- `git diff --check`

## Manual verification

- Seed at least two assessment sessions with the same weak topic and verify a small-group recommendation appears.
- Open `/dashboard` and verify teacher insight cards plus grouped recommendation cards render.
- Call `/api/v1/assessment/diagnosis/{session_id}` for a seeded assessment and inspect the structured payload.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- This lane owns only the Wave 1 evidence spine files listed above.
- Do not expand into spec authoring, prompt assembly, or marketplace work in this lane.
- If scope expands beyond the listed files, update this packet before implementation.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if the new evidence spine becomes part of the shipped product map.

## Handoff notes

- This lane executes the approved `Wave 1 spine` subproject from `docs/superpowers/plans/2026-04-26-contest-mvp-spine-implementation.md`.
