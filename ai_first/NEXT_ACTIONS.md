# Next Actions

Last updated: 2026-04-30

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Execute `C220_CONTEST_LAYOUT_BREAKAGE_SWEEP` from `main`, starting with `/agents` spec-pack authoring and then verifying `/`, `Knowledge`, `Marketplace`, and `Dashboard`.
2. Execute `C221_CONTEST_VIETNAMESE_COVERAGE_COMPLETION` after the layout sweep so longer Vietnamese strings land on stable responsive containers.
3. Decide whether a new browser screenshot recapture packet is needed after those UI-visible fixes merge.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review IP commitment, product-description wording, optional video requirement, and final submission sign-off after `C220/C221` close the remaining visible UI issues.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
## 2026-04-30

1. `C220` is the first follow-up lane because layout breakage currently blocks a credible classroom demo more than wording drift alone.
2. `C221` should follow `C220`, not precede it, because the Vietnamese pass will lengthen labels and needs the responsive containers fixed first.
3. Keep contest wording at validated-prototype level unless a stronger repository artifact is added.
4. Open a new browser-recapture packet only if `C220` or `C221` makes the authoritative screenshot rows stale again.
5. Return to human-only sign-off work only after the current visible UI/runtime follow-ups are merged.
