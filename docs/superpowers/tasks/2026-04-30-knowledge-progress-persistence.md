# Task Packet: Knowledge Progress Persistence

- Task ID: `BUG_KNOWLEDGE_PROGRESS_PERSISTENCE`
- Commit tag: `BUG-KB-PROGRESS`
- Date: 2026-04-30
- Branch: `fix/knowledge-progress-persistence`
- Worktree: `.worktrees/fix-knowledge-progress-persistence`
- Status: Implemented

## Objective

Fix the knowledge-pack indexing status bug so the backend keeps `status/progress` stable in `kb_config.json`, and the API can still return correct progress when the config entry is stale but `.progress.json` exists.

## User-Approved Scope

- fix the root cause that drops `status/progress` from KB config
- recover correct API output for existing KBs that already have `.progress.json`
- avoid changing the `/knowledge` frontend lane unless a narrow contract tweak becomes strictly necessary

## Owned Files

- `deeptutor/services/config/knowledge_base_config.py`
- `deeptutor/knowledge/manager.py`
- `deeptutor/knowledge/progress_tracker.py`
- `deeptutor/api/routers/knowledge.py`
- `tests/api/test_knowledge_router.py`
- `tests/knowledge/test_progress_tracker.py`
- any new focused backend regression tests added for this bug
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-knowledge-progress-persistence.md`
- `docs/superpowers/specs/2026-04-30-knowledge-progress-persistence-design.md`
- `docs/superpowers/plans/2026-04-30-knowledge-progress-persistence.md`
- `docs/superpowers/pr-notes/2026-04-30-knowledge-progress-persistence.md`

## Do-Not-Touch

- `web/app/(utility)/knowledge/page.tsx` unless backend-only recovery proves impossible
- unrelated `/agents`, `/dashboard`, `/playground` runtime lanes
- repo-global environment or model-catalog setup

## Design before implementation

- Runtime behavior change: yes
- Current behavior:
  - indexing progress is persisted to `.progress.json`
  - `status/progress` in `data/knowledge_bases/kb_config.json` can disappear after later config writes
  - API list/info reads from `kb_config.json`, so the UI falls back to `Đang cập nhật trạng thái` and `0%`
- Intended behavior change:
  - KB config writes must preserve existing runtime status/progress fields
  - list/detail APIs must recover from stale config by reading `.progress.json` when needed
- Candidate approach A:
  - fix only `KnowledgeBaseConfigService` overwrite behavior
- Candidate approach B:
  - fix overwrite behavior and add manager/API fallback from `.progress.json`
- Chosen approach and reason:
  - approach B; it fixes future writes and also repairs current user-visible state without manual data surgery

## Required code reading

- Entry points/handlers to inspect:
  - `deeptutor/api/routers/knowledge.py`
- Primary logic/service/use-case modules to inspect:
  - `deeptutor/knowledge/manager.py`
  - `deeptutor/services/config/knowledge_base_config.py`
  - `deeptutor/knowledge/progress_tracker.py`
- Shared contracts/schemas/types to inspect:
  - knowledge list/info payload shape returned to the FE
- Adjacent or reused flows to inspect:
  - metadata update route `PUT /api/v1/knowledge/{kb_name}/config`
  - initialization/upload progress persistence paths
- Existing tests to inspect:
  - `tests/api/test_knowledge_router.py`
  - `tests/knowledge/test_progress_tracker.py`

## Impact surface and stop conditions

- Expected affected areas:
  - centralized KB config writes
  - KB info/read path
  - progress recovery for list/detail APIs
- Files/modules likely to change:
  - `knowledge_base_config.py`
  - `manager.py`
  - `knowledge.py` router
  - focused backend tests
- Files/modules reviewed but expected to remain unchanged:
  - `/knowledge` frontend page
  - `web/lib/knowledge-api.ts`
- Minimum validation paths before the task can stop:
  - config updates no longer delete `status/progress`
  - a KB with only `.progress.json` still returns useful `progress/status`
  - existing create/upload flows still persist completed/error states correctly

## Acceptance criteria

- updating KB metadata does not erase runtime `status/progress`
- list/detail API returns completed/error progress for stale KB entries when `.progress.json` exists
- the bug is covered by backend regression tests

## Required tests

- `pytest tests/knowledge/test_progress_tracker.py tests/api/test_knowledge_router.py -q`

## Implementation notes

- `KnowledgeBaseConfigService.set_kb_config()` now reloads the latest `kb_config.json` before applying metadata updates, so a stale singleton snapshot no longer wipes out runtime `status/progress`.
- `KnowledgeBaseManager.get_info()` now falls back to `data/knowledge_bases/<kb>/.progress.json` when config progress is missing, and derives `ready/error/processing` from the persisted progress stage.
- The `/knowledge` frontend route and `web/lib/knowledge-api.ts` were reviewed but intentionally left unchanged because the existing UI recovers as soon as the API returns stable `status/progress` again.

## Verification run

- `pytest tests/knowledge/test_progress_tracker.py tests/api/test_knowledge_router.py -q`
- `git diff --check`

## Handoff notes

- This lane fixes future writes and recovers current stale KB entries such as local packs that already have `.progress.json` but lost `status/progress` in `kb_config.json`.
- It does not resolve runtime model-catalog issues; KBs that truly failed indexing still surface as `error` once the API fallback reads their progress file.
