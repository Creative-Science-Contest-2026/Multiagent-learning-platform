# Next Actions

Last updated: 2026-04-25

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Capture a fresh screenshot bundle for the contest-facing UI changed by `T044`, `T045`, and `T046`.
2. Update `docs/contest/EVIDENCE_CHECKLIST.md` from `Stale` to `Current` only after the new screenshot capture exists.
3. Keep `docs/contest/VALIDATION_REPORT.md` as the latest command-backed smoke record.
4. Treat any future smoke failure as the next product task before opening another polish slice.
5. Use `ai_first/ACTIVE_ASSIGNMENTS.md` before starting any new lane or docs sync.
6. Keep `ai_first/EXECUTION_QUEUE.md` current after merges, smoke passes, screenshot refreshes, lane changes, and blocker changes.
7. Review IP commitment, final product description wording, and optional video requirements in parallel with the remaining screenshot/human evidence step.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review product scope changes, credential/deployment decisions, or PRs marked blocked by the AI worker.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
