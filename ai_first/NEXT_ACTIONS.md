# Next Actions

Last updated: 2026-04-30

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. If splitting work across sessions, give the safest parallel lane to `C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD`.
2. Use `C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY` as the next runtime-facing follow-up so the new shell and cockpit copy match the contest story.
3. If final judge-facing freshness matters more, recapture the stale Knowledge, Tutor, Dashboard, and `/agents` browser screenshots from `main`.
4. Complete human review of the submission package, IP commitment, and final product-description wording.
5. Decide whether an optional contest video artifact is required.
6. Complete final package sign-off using the current `docs/contest/` read path.

## After Milestone 0

1. Keep the main system map updated when shared contracts change.
2. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
3. Keep CI green and treat CI failures as the next task before starting another runtime/product feature.
4. Preserve lane ownership boundaries so two-account parallel execution stays low-conflict.

## Human Review Needed

- Review IP commitment, product-description wording, optional video requirement, screenshot freshness expectations, and final submission sign-off.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
## 2026-04-30

1. Start new AI sessions from `main` only if a new task packet is explicitly opened.
2. Use `C219` for docs-only parallel work and `C218` for the next bounded runtime wording pass.
3. If no packet exists and the remaining work is human-only, stop instead of inventing a new AI lane.
4. Keep contest wording at validated-prototype level unless a stronger repository artifact is added.
5. Reuse or replace the browser-recapture packet only after confirming whether the authoritative contest evidence docs still mark the screenshot rows stale.
