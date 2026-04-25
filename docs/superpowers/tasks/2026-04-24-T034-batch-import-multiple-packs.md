# Feature Pod Task: Batch Import Multiple Packs

Owner: Codex
Branch: `pod-a/t034-batch-import`
GitHub Issue: `#90`

## Goal

Add a lightweight batch-import slice so teachers can select multiple marketplace packs and import them in one action without repeating the single-pack flow manually.

## User-visible outcome

- Marketplace cards support multi-select for pack import.
- Teachers can trigger one batch action and get per-pack success or failure feedback.
- Existing single-pack import remains available and backward-compatible.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/lib/marketplace-api.ts`
- `deeptutor/api/routers/marketplace.py` only if the selected slice needs backend batch orchestration
- `tests/api/test_marketplace_router.py` and any focused frontend-adjacent regression coverage
- `docs/superpowers/tasks/2026-04-24-T034-batch-import-multiple-packs.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Dashboard, tutoring, assessment review, and knowledge-pack versioning flows
- Unrelated API routers and session persistence code
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files

## API/data contract

- Preserve the existing single-pack import behavior.
- Prefer reusing the current import path and response shape where possible.
- If a batch endpoint is added, keep the payload small and deterministic: explicit pack list in, per-pack status out.

## Acceptance criteria

- Marketplace UI supports selecting multiple packs and clearing the selection.
- One user action can import the selected set and report which imports succeeded or failed.
- Existing single-pack import flow still works.
- Regression coverage exists for the chosen backend/client batch behavior.

## Required tests

- Marketplace router regression coverage for the selected batch-import slice
- Frontend production build verification if marketplace UI or client typing changes

## Manual verification

- Select at least two public packs in marketplace
- Trigger batch import once
- Confirm imported packs appear in the user workspace and the selection resets or reflects completion cleanly

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T033` merged to `main` through PR `#89`.
- Start by reading the current single-pack import flow in marketplace UI and API client; keep the first batch slice minimal and reuse the existing import behavior instead of inventing a second import stack.
