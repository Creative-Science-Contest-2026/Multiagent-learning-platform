# Next Actions

Last updated: 2026-04-25

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Finish the post-lane sync for `T047` and `T048`.
2. Run the demo-readiness smoke flow against the merged `T044`-`T051` product state.
3. Use `docs/contest/DEMO_DATA_RESET.md` before smoke when demo-safe Knowledge Pack or session state may be stale.
4. Update `docs/contest/VALIDATION_REPORT.md` and evidence freshness mirrors if smoke findings or artifact timestamps changed.
5. Treat any smoke failure as the next product task before opening another polish slice.
6. Use `ai_first/ACTIVE_ASSIGNMENTS.md` before starting or switching any new lane or docs sync.
7. Keep `ai_first/EXECUTION_QUEUE.md` current after merges, smoke passes, lane changes, and blocker changes.
8. Review IP commitment, final product description wording, and optional video requirements in parallel with the smoke/evidence lane.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review product scope changes, credential/deployment decisions, or PRs marked blocked by the AI worker.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
