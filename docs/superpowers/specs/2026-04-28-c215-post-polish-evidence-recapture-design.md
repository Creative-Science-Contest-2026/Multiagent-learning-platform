# C215 Post-Polish Evidence Recapture Design

## Goal

Realign contest evidence docs after the Phase 2 polish merges so screenshot freshness states match reality instead of overstating recapture coverage.

## Scope

- Evidence and validation docs only.
- No new smoke run, no browser recapture, no runtime edits.
- Record `C214` completion and `C215` activation in the AI-first mirrors.

## Owned files

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-c215-post-polish-evidence-recapture.md`
- `docs/superpowers/pr-notes/2026-04-28-c215-post-polish-evidence-recapture.md`

## Do-not-touch

- Screenshot assets
- Command outputs and machine-readable evidence status artifact
- Product/runtime code

## Decision

- Keep 2026-04-28 command-backed smoke evidence as `Current`.
- Mark browser screenshots that depict changed UI/copy as `Stale` until a fresh recapture happens.
- Make the operator read path explicit about the difference between command freshness and browser freshness.
