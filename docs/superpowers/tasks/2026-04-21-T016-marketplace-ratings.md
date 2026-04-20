# Feature Pod Task: Add Pack Ratings & Reviews System

Owner: Codex
Branch: `pod-a/t016-marketplace-ratings`
GitHub Issue: `#57`

## Goal

Allow users to rate marketplace knowledge packs and leave short review comments that appear in marketplace listing details.

## User-visible outcome

- Marketplace packs show an average rating and review count.
- Users can submit a 1-5 star rating with an optional short review comment.
- The first version keeps storage simple and local to the existing app data model.

## Owned files/modules

- `web/app/(utility)/marketplace/`
- `web/lib/marketplace-api.ts`
- `deeptutor/api/routers/marketplace.py`
- `tests/api/test_marketplace_router.py`
- `docs/superpowers/tasks/2026-04-21-T016-marketplace-ratings.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-21.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated dashboard, tutor, settings, and notebook files
- Root license and upstream attribution files

## API/data contract

- Extend the marketplace router instead of creating a parallel marketplace service surface
- Keep the first storage model lightweight and deterministic
- Expose only the minimal rating/review payload needed by the marketplace UI

## Acceptance criteria

- Packs expose rating summary data in marketplace responses.
- Users can submit a rating and optional review comment through the API.
- Marketplace UI surfaces average rating and review count cleanly.
- Empty state is handled when a pack has no reviews yet.

## Required tests

- Targeted backend API tests for rating submission and rating summary retrieval
- Frontend build or equivalent validation for touched marketplace UI files

## Manual verification

- Submit a review for a pack from the marketplace UI
- Confirm rating summary updates after submission
- Confirm a never-reviewed pack shows a clean unrated state

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes

- `T015` is merged to `main` through PR `#56`.
- Start from the existing marketplace list/preview/import flow before adding new storage or UI state.
- Implemented on branch `pod-a/t016-marketplace-ratings` with:
  - `POST /api/v1/marketplace/{pack_name}/reviews`
  - rating summary in marketplace list/preview payloads
  - marketplace review display and submission flow in preview modal
- Validation completed:
  - `python3 -m pytest tests/api/test_marketplace_router.py -q`
  - `python3 -m py_compile deeptutor/api/routers/marketplace.py`
  - `cd web && npm run build`
- PR note prepared:
  - `docs/superpowers/pr-notes/2026-04-21-marketplace-ratings.md`
