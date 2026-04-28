# Feature Pod Task: C212 Core Loop Visibility Polish

Task ID: `C212_CORE_LOOP_VISIBILITY_POLISH`
Commit tag: `C212`
Owner: Session C
Branch: `fix/submission-close-session-c`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Make the five-step contest loop more visible across existing teacher-facing product screens with bounded UI polish only.

## User-visible outcome

- Knowledge, Assessment, Tutor, and Dashboard screens visibly map to the same contest loop.
- The current step is obvious without reading contest docs first.
- The dashboard still reads as diagnosis/intervention support, not autonomous judgment.

## Owned files/modules

- `docs/superpowers/specs/2026-04-28-c212-core-loop-visibility-polish-design.md`
- `docs/superpowers/plans/2026-04-28-c212-core-loop-visibility-polish.md`
- `docs/superpowers/tasks/2026-04-28-c212-core-loop-visibility-polish.md`
- `docs/superpowers/pr-notes/2026-04-28-c212-core-loop-visibility-polish.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `web/components/contest/`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`

## Do-not-touch files/modules

- `docs/contest/`
- `ai_first/competition/`
- `deeptutor/`
- `web/app/(workspace)/dashboard/student/page.tsx`
- `web/components/dashboard/TeacherInsightPanel.tsx`
- lockfiles unless a dependency change becomes strictly necessary

## Constraints

- Keep the exact loop wording: `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`.
- Do not add new routes, APIs, or stateful flows.
- Do not widen the polish beyond the four scoped screens and one shared component family.
- Keep mobile layout safe and avoid a forced horizontal scroll strip.

## Required tests

- `cd web && npx eslint app/'(utility)'/knowledge/page.tsx app/'(workspace)'/dashboard/page.tsx app/'(workspace)'/dashboard/assessments/[sessionId]/page.tsx app/'(workspace)'/agents/[botId]/chat/page.tsx components/contest/*.tsx`
- `cd web && npm run build`
- `git diff --check`

## PR ownership

- `PR-POLISH-02 Core Loop Visibility Polish`

## Architecture note

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change unless implementation escapes bounded UI polish.
