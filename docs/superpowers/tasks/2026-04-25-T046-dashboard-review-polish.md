# Feature Pod Task: Dashboard and Review Screen Copy and UX Polish

Owner:
Branch: `pod-a/t046-dashboard-review-polish`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Refine the teacher dashboard, assessment review, and tutor replay screens so the contest demo path reads like one coherent workflow.

## User-visible outcome

- Dashboard sections have clearer labels and empty states.
- Assessment review explains progress and next actions more cleanly.
- Tutor replay reads as a deliberate teacher-facing review surface instead of a raw transcript page.

## Owned files/modules

- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/dashboard/student/page.tsx`
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `web/app/(workspace)/dashboard/sessions/[sessionId]/page.tsx`
- `web/components/assessment/LearningJourneySummary.tsx`
- `web/components/assessment/ProgressIndicator.tsx`

## Do-not-touch files/modules

- `deeptutor/api/routers/`
- `deeptutor/services/`
- `web/lib/`
- `web/locales/vi/`
- `ai_first/`

## API/data contract

Use existing dashboard, review, and replay contracts only.

## Acceptance criteria

- Dashboard and review surfaces present clearer next-step messaging.
- Empty states and supporting labels feel intentional and teacher-readable.
- The slice remains frontend-only.

## Required tests

- `cd web && npm run build`
- `git diff --check`

## Manual verification

- Open dashboard overview, student dashboard, assessment review, and tutor replay.
- Confirm the copy and information hierarchy feel polished and consistent.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not change `web/lib/dashboard-api.ts` or backend response shapes in this slice.
- If UI polish reveals a contract gap, hand it off to Lane 2 rather than widening scope.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated unless route behavior changes materially.

## Handoff notes
