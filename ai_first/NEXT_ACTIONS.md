# Next Actions

Last updated: 2026-04-19

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Merge the docs-only CI task packet PR when eligible.
2. Open and merge the CI implementation PR from `fix/ci-backend-frontend-checks`.
3. If any required backend, frontend, or docs check fails, fix that CI failure before starting another feature.
4. Keep GitHub issues `#2`, `#3`, `#9`, `#12`, and `#16` linked to their implementation PRs.
5. Preserve unrelated dirty files until they are intentionally handled.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep reliable backend, frontend, and docs CI checks as the gate before broader runtime auto-merge.

## Human Review Needed

- Review product scope changes, credential/deployment decisions, or PRs marked blocked by the AI worker.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
