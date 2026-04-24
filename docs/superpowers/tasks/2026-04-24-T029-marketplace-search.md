# Feature Pod Task: Marketplace Full-Text Search

Owner: Codex
Branch: `pod-a/t029-marketplace-search`
GitHub Issue: `#79`

## Goal

Improve marketplace search so teachers can discover packs through broader metadata and lightweight content signals, not only narrow name matches.

## User-visible outcome

- Marketplace search matches pack name, owner, subject, curriculum, learning objectives, and other compact metadata signals.
- Search remains compatible with the existing marketplace filters, sorting, cache, and pagination flow.
- The first slice stays lightweight and does not require a dedicated full-text index.

## Owned files/modules

- `deeptutor/api/routers/marketplace.py`
- `web/lib/marketplace-api.ts`
- `web/app/(utility)/marketplace/page.tsx`
- `tests/api/test_marketplace_router.py`
- `docs/superpowers/tasks/2026-04-24-T029-marketplace-search.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md` if created, otherwise `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Dashboard, tutor, knowledge, and settings features
- Unrelated API routers
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve the current marketplace list API shape.
- Extend search behavior inside the existing query/filter path instead of creating a new route family.
- Keep search case-insensitive and deterministic.

## Acceptance criteria

- Marketplace search can match across more than just pack name fragments.
- Search works against compact metadata such as objectives and curriculum.
- Existing list sorting/filtering behavior stays intact.

## Required tests

- Marketplace router regression coverage for the expanded search matching

## Manual verification

- Search for terms found only in metadata/objectives and confirm matching packs appear
- Confirm filters and sort still behave correctly with search applied

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T027` merged to `main` through PR `#78`.
- Keep the first slice metadata-driven before considering a real full-text index.
