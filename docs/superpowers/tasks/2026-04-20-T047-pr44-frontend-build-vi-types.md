# Feature Pod Task: PR #44 Frontend Build Unblock for Vietnamese UI Types

Owner: Codex
Branch: `fix/pr44-frontend-build-vi-types`
GitHub Issue: `#47`

## Goal

Unblock PR #44 by fixing the settings UI type mismatch so the frontend build accepts Vietnamese (`vi`) language preferences consistently.

## User-visible outcome

- Settings page can persist theme and language when the selected language is `vi`.
- Frontend CI for the affected branch no longer fails on the TypeScript compile error.

## Owned files/modules

- `web/app/(utility)/settings/page.tsx`
- Related shared frontend language helper/type files only if the fix requires them
- `web/lib/dashboard-api.ts`
- `docs/superpowers/tasks/2026-04-20-T047-pr44-frontend-build-vi-types.md`
- `docs/superpowers/pr-notes/2026-04-20-pr44-frontend-build-vi-types.md`
- `ai_first/daily/2026-04-20.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated marketplace, dashboard, and backend files

## API/data contract

- No API shape changes
- Keep `/api/v1/settings/ui` payload compatible, only align frontend types with the already-supported `vi` option
- Keep `AssessmentSummary.estimated_time_spent` optional to match the current assessment-review flow

## Acceptance criteria

- `persistUi()` accepts the full supported language union used by the settings page
- Any local helper that writes/persists UI language accepts `vi`
- Assessment review typing no longer blocks the build on optional `estimated_time_spent`
- `cd web && npm run build` passes from a clean checkout on the fix branch
- Diff stays limited to the UI preference/build blocker

## Required tests

- `cd web && npm run build`

## Manual verification

- Open settings UI and inspect the language/theme persistence path for `vi`
- Confirm no new type errors are introduced in the settings and assessment review routes

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.
- Expected: no system-map update unless architecture changed beyond typing alignment.

## Handoff notes

- Base this task from the branch used to validate PR #44 so the fix can be merged back into that PR flow cleanly.
- Keep the PR narrowly scoped to the frontend build blockers only.
