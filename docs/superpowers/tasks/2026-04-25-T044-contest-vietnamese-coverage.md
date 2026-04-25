# Feature Pod Task: Contest MVP Vietnamese Coverage Audit and Fix Pass

Owner:
Branch: `pod-a/t044-vi-contest-coverage`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Close obvious English leakage on contest MVP screens and align Vietnamese wording across the user-facing contest flow.

## User-visible outcome

- Contest MVP screens read coherently in Vietnamese when the locale is set to `vi`.
- Loading, empty, and error states avoid raw English fallback copy.
- Repeated concepts use stable Vietnamese wording across marketplace, knowledge, dashboard, assessment review, and tutor replay.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/dashboard/student/page.tsx`
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
- `web/app/(workspace)/dashboard/sessions/[sessionId]/page.tsx`
- `web/locales/vi/app.json`
- `web/locales/vi/common.json`

## Do-not-touch files/modules

- `deeptutor/api/routers/`
- `deeptutor/services/`
- `web/lib/`
- `ai_first/`

## API/data contract

No backend or API-client contract changes in this slice.

## Acceptance criteria

- No obvious English-only contest labels remain when Vietnamese is selected.
- Vietnamese copy is consistent for Knowledge Pack, assessment, tutor, dashboard, review, and replay.
- The slice remains frontend-only unless the task packet is updated first.

## Required tests

- `rg -n "Loading|Error|Back to Dashboard|Assessment Review|Tutoring Session Replay|Create Knowledge Pack|Marketplace" web/app web/components web/locales/vi -S`
- `cd web && npm run build`
- `git diff --check`

## Manual verification

- Switch the app to Vietnamese.
- Visit marketplace, knowledge, dashboard overview, assessment review, and tutor replay.
- Confirm those contest screens no longer show obvious English fallback strings.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not widen scope into `web/lib/` or backend routers without updating this packet first.
- Coordinate new translation-key needs through the task packet before another lane touches locale files.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated unless screen structure or route behavior materially changes.

## Handoff notes
