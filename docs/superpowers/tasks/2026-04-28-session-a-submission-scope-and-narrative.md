# Feature Pod Task: Session A Submission Scope And Narrative

Task ID: `OPS_SUBMISSION_CLOSE_A`
Commit tag: `OPS-A`
Owner: Session A
Branch: `docs/submission-close-session-a`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Freeze the contest submission story, claims, operator-facing read path, and manual-review skeleton without editing validation-owned files.

## User-visible outcome

- The repo says one clear thing about the product.
- The submission package has one authoritative read path.
- Manual review gates are explicit instead of implied.

## Owned files/modules

- `ai_first/competition/product-description.md`
- `ai_first/competition/fork-modifications.md`
- `ai_first/competition/pitch-notes.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `docs/superpowers/tasks/2026-04-28-session-a-submission-scope-and-narrative.md`

## Do-not-touch files/modules

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/evidence/`
- `deeptutor/`
- `web/`

## PR ownership

- `PR-CLOSE-01 Submission Scope Freeze`
- `PR-CLOSE-02 Claim and Proof Contract Freeze`
- `PR-CLOSE-06 Submission Narrative Pack`
- `PR-CLOSE-07 Submission Operator Pack`
- `PR-CLOSE-08 Human Review Gates`
- `PR-CLOSE-09 Final Package Readiness`

## Dependency notes

- Start `PR-CLOSE-01` immediately.
- Start `PR-CLOSE-02` after `PR-CLOSE-01`.
- Draft `PR-CLOSE-06` in parallel, but do not finalize wording that depends on validation status until Session B lands its proof updates.
- Start `PR-CLOSE-09` only after Session B finishes `PR-CLOSE-05`.

## Output contract

- Keep all claims at validated-prototype level unless Session B refreshes stronger evidence.
- Do not silently widen the product story beyond `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`.
- Keep the final operator read path link-heavy and conflict-light.
