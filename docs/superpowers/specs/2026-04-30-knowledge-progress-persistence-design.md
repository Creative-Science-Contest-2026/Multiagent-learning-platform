# Knowledge Progress Persistence Design

- Date: 2026-04-30
- Task ID: `BUG_KNOWLEDGE_PROGRESS_PERSISTENCE`
- Branch: `fix/knowledge-progress-persistence`

## Goal

Ensure knowledge-pack indexing progress survives later config edits and still shows up through the existing API contract, so the UI stops displaying the generic `Đang cập nhật trạng thái / 0%` fallback for indexed packs.

## Current behavior

- `ProgressTracker` writes authoritative runtime progress into:
  - `data/knowledge_bases/<kb>/.progress.json`
  - `data/knowledge_bases/kb_config.json` through `KnowledgeBaseManager.update_kb_status()`
- the metadata edit route uses `KnowledgeBaseConfigService.set_kb_config()`
- `KnowledgeBaseConfigService` saves its in-memory `_config` snapshot without reloading newer runtime fields from disk first
- because `KnowledgeBaseManager` and `KnowledgeBaseConfigService` both write the same JSON file independently, later metadata saves can drop `status/progress`
- `KnowledgeBaseManager.get_info()` currently trusts `kb_config.json` for `status/progress`, so once those fields disappear the FE only sees stale or empty progress

## Intended behavior

- metadata updates must preserve existing runtime `status/progress`
- the read path must recover from stale config by reading `.progress.json` when config progress is absent
- completed/error states already stored for current KBs should become visible again without requiring a fresh reindex

## Approaches

### Approach A: writer-side fix only

- reload latest config in `KnowledgeBaseConfigService` before save
- merge new metadata onto the latest on-disk entry
- Pros:
  - smallest write-path change
- Cons:
  - does not recover already-broken KB entries unless they are rewritten again

### Approach B: writer-side fix plus read fallback

- make `KnowledgeBaseConfigService` reload the latest file before mutating and preserve runtime fields
- add a fallback in `KnowledgeBaseManager.get_info()`:
  - if `kb_config.json` lacks useful `status/progress`
  - inspect `.progress.json`
  - derive `status` from progress stage when possible
- Pros:
  - fixes future writes
  - repairs current user-visible state immediately
- Cons:
  - slightly broader impact surface

## Chosen approach

Approach B.

It addresses the root cause and recovers existing broken KB entries without requiring manual config surgery or frontend changes.

## Planned changes

### 1. Make KB config writes reload-safe

- In `KnowledgeBaseConfigService.set_kb_config()`:
  - reload the latest `kb_config.json` from disk before mutating
  - merge the requested metadata into the newest KB entry instead of the stale in-memory copy
  - preserve runtime fields such as:
    - `status`
    - `progress`
    - `updated_at`
    - any other non-metadata runtime state already present

### 2. Add progress fallback on the read path

- In `KnowledgeBaseManager.get_info()`:
  - if config has no `progress`, or status is missing/unknown while `.progress.json` exists
  - read `.progress.json`
  - use that progress as the returned `progress`
  - derive a returned `status` from stage when config status is absent:
    - `completed` -> `ready`
    - `error` -> `error`
    - in-progress stages -> `processing`

### 3. Keep current API contract stable

- `GET /api/v1/knowledge/list` and `GET /api/v1/knowledge/{kb_name}` should keep returning the same top-level fields:
  - `status`
  - `progress`
- no frontend route changes should be required for the UI to recover

## Expected files to change

- `deeptutor/services/config/knowledge_base_config.py`
- `deeptutor/knowledge/manager.py`
- `tests/api/test_knowledge_router.py`
- `tests/knowledge/test_progress_tracker.py`

## Expected files reviewed but left unchanged

- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/knowledge-api.ts`
- `deeptutor/knowledge/progress_tracker.py` unless a small helper extraction becomes useful

## Validation

- update KB metadata after a completed index run and confirm `status/progress` remain in config or API output
- create a stale config scenario where `.progress.json` exists but config progress is missing, and confirm list/info API still returns useful progress
- run focused backend regression tests
