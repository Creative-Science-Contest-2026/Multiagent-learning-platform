# Feature Pod Task: Knowledge and Marketplace Metadata Depth Pass

Owner:
Branch: `pod-b/t049-metadata-depth`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Deepen teacher-facing pack metadata and marketplace detail contracts so metadata quality feels more complete without redesigning the product.

## User-visible outcome

- Marketplace preview exposes richer teacher-useful detail.
- Knowledge Pack metadata feels more complete and informative.
- The UI has cleaner data to render without forcing same-PR page rewrites.

## Owned files/modules

- `deeptutor/api/routers/knowledge.py`
- `deeptutor/api/routers/marketplace.py`
- `deeptutor/knowledge/manager.py`
- `web/lib/knowledge-api.ts`
- `web/lib/marketplace-api.ts`
- `tests/api/test_knowledge_router.py`
- `tests/api/test_marketplace_router.py`
- `tests/knowledge/test_kb_metadata_normalization.py`

## Do-not-touch files/modules

- `web/app/(utility)/marketplace/`
- `web/app/(utility)/knowledge/`
- `web/app/(workspace)/dashboard/`
- `web/locales/vi/`
- `ai_first/`

## API/data contract

This slice may expand metadata fields, but all additions must remain backward compatible and documented in the PR note.

## Acceptance criteria

- Metadata and preview contracts expose richer teacher-useful detail.
- Existing clients remain compatible.
- Added fields are covered by targeted tests.

## Required tests

- `python3 -m pytest tests/api/test_knowledge_router.py tests/api/test_marketplace_router.py tests/knowledge/test_kb_metadata_normalization.py -q`
- `python3 -m py_compile deeptutor/api/routers/knowledge.py deeptutor/api/routers/marketplace.py deeptutor/knowledge/manager.py`
- `git diff --check`

## Manual verification

- Confirm API payloads still load for existing packs.
- Confirm new metadata fields are additive rather than breaking.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Do not modify Lane 1 page components in this slice.
- If frontend changes become necessary, document the contract and hand off to Lane 1 in a later packet update.

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if data-contract or workflow structure changes materially.

## Handoff notes
