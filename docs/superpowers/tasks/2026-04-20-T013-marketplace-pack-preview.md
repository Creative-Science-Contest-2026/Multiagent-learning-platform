# Feature Pod Task: Marketplace Pack Preview Modal

Owner: Codex
Branch: `pod-a/t013-marketplace-pack-preview`
GitHub Issue: `#51`

## Goal

Add a preview flow on the Marketplace page so teachers can inspect a pack before importing it.

## User-visible outcome

- Marketplace cards expose a preview action.
- Users can open a modal or detail panel showing metadata, learning objectives, and a compact sample of pack contents.
- Preview errors are surfaced without interrupting the browse/import flow.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/lib/marketplace-api.ts`
- `deeptutor/api/routers/marketplace.py`
- `docs/superpowers/tasks/2026-04-20-T013-marketplace-pack-preview.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-20.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated dashboard, tutoring, and settings files

## API/data contract

- Add a marketplace preview read endpoint under `deeptutor/api/routers/marketplace.py`
- Keep existing list/import endpoints stable
- Preview payload should stay compact and deterministic for the UI

## Acceptance criteria

- Marketplace UI shows a preview action for shareable packs.
- Preview fetch returns metadata, learning objectives, and a concise content summary.
- Loading and error states are handled cleanly in the preview flow.
- Existing import flow continues to work unchanged.

## Required tests

- Targeted backend test coverage for the preview route
- Frontend build/lint validation for touched marketplace files

## Manual verification

- Open Marketplace page.
- Trigger preview for a shareable pack.
- Confirm preview content renders and closes correctly.
- Confirm import still works after preview interaction.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T012` was verified as already implemented on `main`; this task is now the next active registry item.
- Build the smallest useful preview payload first; avoid turning preview into a second full import/details page.
