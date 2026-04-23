# Feature Pod Task: Marketplace List Caching & Pagination Optimization

Owner: Codex
Branch: `pod-a/t023-marketplace-cache-optimization`
GitHub Issue: `#69`

## Goal

Improve marketplace browsing performance by caching list responses on the client and reducing disruptive full-list reloads during pagination.

## User-visible outcome

- Marketplace browsing reuses recent list results instead of refetching identical queries on every revisit.
- Marketplace list supports progressive loading for additional packs without replacing already visible results.
- Existing marketplace filters, sorting, preview, rating, and import flows continue to work.

## Owned files/modules

- `web/app/(utility)/marketplace/page.tsx`
- `web/lib/marketplace-api.ts`
- `docs/superpowers/tasks/2026-04-23-T023-marketplace-cache-optimization.md`
- `docs/superpowers/pr-notes/` for the follow-up PR note
- `ai_first/TASK_REGISTRY.json`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-23.md`

## Do-not-touch files/modules

- Dashboard, tutor, assessment, and settings files
- `deeptutor/core/`
- `deeptutor/runtime/`
- Root license and upstream attribution files
- Backend marketplace router unless frontend changes prove an API contract gap

## API/data contract

- Reuse the existing `GET /api/v1/marketplace/list` endpoint.
- Keep current list response shape backward-compatible.
- Implement cache and stale refresh behavior on the client without requiring new server dependencies.

## Acceptance criteria

- Marketplace list avoids unnecessary refetches for repeated list queries during a short browsing session.
- Marketplace users can progressively load additional packs while preserving already rendered results.
- Existing filters and sorting keep returning the correct list contents.

## Required tests

- Frontend production build verification
- Any targeted automated coverage added for cache helpers, if introduced

## Manual verification

- Open marketplace and confirm first page loads normally
- Change sorting or filters and confirm list updates correctly
- Revisit a recent query and confirm cached results appear without a visible full reset
- Load more packs and confirm earlier cards remain visible

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

## Handoff notes

- `T021` merged to `main` through PR `#68`.
- Start by inspecting `web/lib/marketplace-api.ts` and `web/app/(utility)/marketplace/page.tsx`; the current flow refetches each page with `cache: "no-store"` and replaces the visible list on pagination.
- Prefer a lightweight in-repo cache over adding a new dependency for this task size.
