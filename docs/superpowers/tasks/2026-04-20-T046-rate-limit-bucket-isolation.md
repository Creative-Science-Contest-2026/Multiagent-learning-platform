# Feature Pod Task: Rate-Limit Bucket Isolation for PR #44 Middleware

Owner: Codex
Branch: `fix/pr44-rate-limit-bucket-isolation`
GitHub Issue: `#46`

## Goal

Correct the HTTP rate-limit middleware so counters are isolated by the matched policy instead of colliding across different marketplace routes.

## User-visible outcome

- Bursts of marketplace import requests do not incorrectly throttle marketplace list/detail reads.
- Route-specific rate-limit rules behave as documented.

## Owned files/modules

- `deeptutor/api/main.py`
- `tests/api/test_rate_limit_middleware.py`
- `docs/superpowers/tasks/2026-04-20-T046-rate-limit-bucket-isolation.md`
- `docs/superpowers/pr-notes/2026-04-20-pr44-rate-limit-bucket-isolation.md`
- `ai_first/daily/2026-04-20.md`

## Do-not-touch files/modules

- `deeptutor/core/`
- `deeptutor/runtime/`
- Unrelated frontend files

## API/data contract

- Keep existing `429` response shape and `Retry-After` header behavior
- Preserve declared limits while changing only how the bucket key is derived/stored

## Acceptance criteria

- Requests matching different policies do not share the same counter bucket unless intended
- Marketplace import and marketplace list can no longer collide through a shared key
- Regression coverage proves the intended bucket split
- Relevant backend validation passes

## Required tests

- `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m pytest tests/api/test_rate_limit_middleware.py -q`
- `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m py_compile deeptutor/api/main.py`

## Manual verification

- Verify the computed key/policy for `/api/v1/marketplace/import/...` differs from `/api/v1/marketplace/list`
- Confirm fallback `/api/v1` policy still works for unrelated routes

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.
- Expected: no system-map update unless the middleware architecture changes materially.

## Handoff notes

- This branch is based on `fix/pr44-frontend-build-vi-types` so it can merge after the CI-unblock PR in the PR #44 follow-up stack.
- Keep the PR narrowly scoped to bucket isolation and regression coverage.
