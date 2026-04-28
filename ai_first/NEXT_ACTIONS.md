# Next Actions

Last updated: 2026-04-28

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Complete human review of the submission package, IP commitment, and final product-description wording.
2. Decide whether an optional contest video artifact is required.
3. Review the refreshed browser screenshot bundle from `docs/post-phase2-browser-recapture-run` and merge it once validation and CI are green.
4. Complete final package sign-off using the current `docs/contest/` read path.
5. Treat any future smoke failure as the next product task before opening another lane.
6. Use `ai_first/ACTIVE_ASSIGNMENTS.md` before starting any new AI lane or docs sync.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review IP commitment, product-description wording, optional video requirement, and final submission sign-off.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
## 2026-04-28

1. Start new AI sessions from `main` only if a new task packet is explicitly opened.
2. Use the matching packet before code edits.
3. If no packet exists and the remaining work is human-only, stop instead of inventing a new AI lane.
4. Keep contest wording at validated-prototype level unless a stronger repository artifact is added.
5. Reuse the post-Phase-2 browser recapture packet if a future UI change makes the current screenshot bundle stale again.
