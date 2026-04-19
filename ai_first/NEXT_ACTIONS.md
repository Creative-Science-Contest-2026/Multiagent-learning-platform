# Next Actions

Last updated: 2026-04-19

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Keep `ai_first/EXECUTION_QUEUE.md` current after merges and blocker changes.
2. Create the contest submission package from issue `#41`.
3. Link the pitch, demo story, evidence checklist, validation report, screenshots, smoke notes, known limitations, and final submission checklist from one short read path.
4. Review whether optional video capture is required after the package exists.
5. Use `docs/contest/DEMO_DATA_RESET.md` before smoke when demo-safe Knowledge Pack or session state may be stale.
6. If a future smoke fails, create or update the next focused product/runtime bug task from the first hard failure.
6. Keep open issues aligned with active task packets and unfinished work only.
7. Preserve unrelated dirty files until they are intentionally handled.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.

## Human Review Needed

- Review product scope changes, credential/deployment decisions, or PRs marked blocked by the AI worker.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
