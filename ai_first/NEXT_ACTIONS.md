# Next Actions

Last updated: 2026-04-30

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Resume human review and final submission sign-off now that `C221_CONTEST_VIETNAMESE_COVERAGE_COMPLETION` is merged.
2. Decide whether a new browser screenshot recapture packet is needed after the post-`C221` Vietnamese UI changes.
3. Keep CI green and treat any follow-up contest-doc freshness gap as a new packet, not an implicit continuation.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review IP commitment, product-description wording, optional video requirement, and final submission sign-off now that `C221` has closed the last visible UI issue.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
## 2026-04-30

1. `C220` and `C221` are merged, so no AI-owned runtime recovery lane remains open on the contest path.
2. Keep contest wording at validated-prototype level unless a stronger repository artifact is added.
3. Open a new browser-recapture packet only if `C221` makes the authoritative screenshot rows stale enough to require refreshed evidence.
4. Treat the remaining contest work as human review unless a new packet is explicitly opened.
