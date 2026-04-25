# Feature Pod Task: Offline Mode for Downloaded Packs

Owner: Codex
Branch: `pod-a/t035-offline-mode`
GitHub Issue: `#92`

## Goal

Add a first offline-capable slice so imported packs remain usable when the network drops and quiz completion can queue its result sync until connectivity returns.

## User-visible outcome

- Imported/downloaded packs remain visible from a local browser cache even if the API is unavailable.
- Users can still finish an already loaded assessment while offline.
- Quiz result recording retries automatically when the browser comes back online.

## Owned files/modules

- `web/lib/marketplace-api.ts`
- `web/lib/knowledge-api.ts`
- `web/lib/session-api.ts`
- `web/components/quiz/QuizViewer.tsx`
- `web/app/(workspace)/page.tsx` only if lightweight offline status or fallback handling is needed
- `docs/superpowers/tasks/2026-04-24-T035-offline-mode-support.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Backend routers and storage schemas unless the selected slice truly needs them
- Dashboard, tutoring, and knowledge-pack versioning flows
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve current online behavior for marketplace import, knowledge-base listing, and quiz result recording.
- Prefer browser-local persistence for the first slice instead of introducing server-side offline state.
- Keep offline state deterministic and scoped to imported packs plus pending quiz-result sync.

## Acceptance criteria

- Imported packs are cached locally after import and can be surfaced when knowledge-base listing fails offline.
- Completing a loaded quiz offline does not lose the result payload.
- Pending offline quiz results retry automatically when the browser is online again.
- Existing online flows remain unchanged when the network is available.

## Required tests

- Focused frontend-safe validation through production build
- Targeted regression coverage for any added pure helper behavior when feasible

## Manual verification

- Import at least one marketplace pack while online
- Simulate offline browser state
- Confirm the imported pack still appears in the KB selection surface
- Complete a loaded quiz offline and verify sync occurs after reconnect

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T034` merged to `main` through PR `#91`.
- Keep the first slice browser-local and reversible; do not try to build a full PWA stack in one pass.
