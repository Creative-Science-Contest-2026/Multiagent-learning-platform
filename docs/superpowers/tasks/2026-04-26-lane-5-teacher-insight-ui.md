# Feature Pod Task: Lane 5 Teacher Insight UI

Task ID: `L5_TEACHER_INSIGHT_UI`
Commit tag: `L5`
Owner: Session-specific
Branch: `pod-a/teacher-insight-ui`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Turn the merged Wave 1 teacher insight surface into a clearer teacher workflow that distinguishes facts, diagnosis, and next actions.

## User-visible outcome

- Teachers can inspect per-student evidence, diagnosis, and recommendation without ambiguity.
- The dashboard supports small-group views and richer action surfaces.
- The UI presents evidence-backed insight rather than a decorative analytics shell.

## Owned files/modules

- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/dashboard/student/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- `web/components/dashboard/`
- `web/lib/dashboard-api.ts`
- `tests` only if frontend-specific test coverage is added in scope
- `docs/superpowers/tasks/2026-04-26-lane-5-teacher-insight-ui.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `deeptutor/services/evidence/`
- `deeptutor/services/session/`
- `deeptutor/api/routers/assessment.py`
- `deeptutor/api/routers/dashboard.py` unless an API contract bug blocks UI work and the human approves scope expansion

## API/data contract

- Consume the structured insight payload already merged in Wave 1 or its later compatible evolution from Lane 4.
- Keep `Observed`, `Inferred`, and `Recommended Action` visually separate.
- Do not invent new AI claims in the UI layer.

## Acceptance criteria

- Dashboard clearly distinguishes evidence facts from diagnosis claims.
- Per-student insight and small-group recommendations are usable on both desktop and mobile.
- UI supports next-step teacher actions and clear evidence trace display.
- The lane does not embed diagnosis logic in the frontend.

## Required tests

- Frontend lint/build checks for owned dashboard files
- Any targeted component tests added in scope
- `git diff --check`

## Manual verification

- Open `/dashboard` with seeded insight data and verify evidence, diagnosis, and actions render distinctly.
- Check mobile layout for teacher insight cards and grouped recommendations.
- Verify no UI element implies certainty beyond the payload’s confidence/evidence.

## Parallel-work notes

- Start from merged Wave 1 UI on `main`.
- This lane owns presentation and workflow, not diagnosis semantics.
- If the payload is insufficient for the intended UX, ask the human whether Lane 4 should extend it before editing backend code here.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the teacher workflow surface changes the top-level product map materially.

## Handoff notes

- This is Session = Lane 5.
- Keep visual language aligned with existing dashboard patterns unless the human explicitly asks for redesign.
- Treat backend payloads as contracts, not suggestions.
- Implemented the evidence-first workflow without changing backend diagnosis semantics or router contracts.
- `/dashboard/student` now uses the dashboard insight payload plus existing progress context; deeper evidence traces should be added in a future backend lane if needed.
- Do not compensate for missing payload fields with frontend-only inference.
