# Feature Pod Task: Marketplace Sorting Options

Owner: Codex
Branch: `pod-a/t019-marketplace-sorting`
GitHub Issue: `#63`

## Goal

Add marketplace sorting options so users can reorder packs by popularity, recency, rating, and objective count.

## User-visible outcome

- Marketplace users can choose a sort mode from the UI.
- Sorting is applied by the API, not only client-side reshuffling.
- Existing default ordering remains stable when no explicit sort is selected.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/lib/marketplace-api.ts`
- `deeptutor/api/routers/marketplace.py`
- `tests/api/test_marketplace_router.py`
- `docs/superpowers/tasks/2026-04-21-T019-marketplace-sorting.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- Assessment, dashboard, tutor, and settings files
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Extend `GET /api/v1/marketplace/list` with a `sort_by` query parameter.
- Support at least:
  - `popularity`
  - `recent`
  - `rating`
  - `most_objectives`
- Keep payload shape backward-compatible.

## Acceptance criteria

- Users can select sort options from the marketplace UI.
- API-backed sorting returns packs in the expected order for each supported mode.
- Default marketplace behavior remains backward-compatible when `sort_by` is omitted.

## Required tests

- API regression coverage for supported `sort_by` values
- Relevant frontend validation if client wiring changes need build verification

## Manual verification

- Open marketplace page
- Switch between sort modes
- Confirm card ordering changes accordingly

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T018` merged to `main` through PR `#62`.
- Baseline worktree marketplace test currently errors at collection because this worktree lacks `data/user/settings/main.yaml`; treat that as environment setup debt, not a `T019` regression.
- Worktree-local runtime settings were normalized with a local symlink so baseline tests and frontend build could run in this lane.
- Implemented API-backed `sort_by` support and wired marketplace UI sorting to it.
- Validation:
  - `python3 -m pytest tests/api/test_marketplace_router.py -q`
  - `python3 -m py_compile deeptutor/api/routers/marketplace.py`
  - `cd web && npm run build`
