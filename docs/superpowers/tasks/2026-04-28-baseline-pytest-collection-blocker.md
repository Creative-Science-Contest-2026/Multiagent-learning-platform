# Feature Pod Task: Baseline Pytest Collection Blocker

Task ID: `OPS_PYTEST_COLLECTION_BLOCKER`
Commit tag: `OPS-PYTEST`
Owner: Session-specific
Branch: `fix/baseline-pytest-collection-blocker`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Fix the current baseline `pytest` collection failure on `main` so the full suite can at least collect tests consistently before any higher-level workflow or docs branch is merged.

## User-visible outcome

- `pytest -q` no longer stops at collection time with `import file mismatch`.
- Duplicate test basenames under `tests/` no longer collide in default pytest import mode.

## Owned files/modules

- `tests/__init__.py`
- `tests/agents/__init__.py`
- `tests/agents/math_animator/__init__.py`
- `tests/agents/research/__init__.py`
- `tests/services/llm/__init__.py`
- `docs/superpowers/tasks/2026-04-28-baseline-pytest-collection-blocker.md`
- `docs/superpowers/pr-notes/2026-04-28-baseline-pytest-collection-blocker.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-28.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/AI_OPERATING_PROMPT.md`
- `docs/contest/`
- `requirements/`
- lockfiles

## API/data contract

- This fix changes test-package layout only.
- It must not change runtime/product behavior.
- It must not switch global pytest import mode as a side effect.

## Acceptance criteria

- `pytest --collect-only -q` completes without `import file mismatch`.
- The fix is limited to package markers or equally small test-layout stabilization.
- Any remaining failing tests are post-collection baseline failures, not collection blockers.

## Required tests

- `pytest --collect-only -q`
- `pytest -q`
- `git diff --check`

## Manual verification

- Confirm the previous `test_request_config` and `test_utils` import mismatch no longer appears.
- Confirm no runtime/product files changed.

## Parallel-work notes

- Keep this lane separate from `docs/submission-close-master`.
- Do not widen this into fixing the 23 post-collection baseline failures.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should not change because this is test-layout stabilization only.

## Handoff notes

- This lane exists only to remove the collection blocker.
- If the suite still has logic/config failures after collection succeeds, report them separately instead of silently expanding scope.
