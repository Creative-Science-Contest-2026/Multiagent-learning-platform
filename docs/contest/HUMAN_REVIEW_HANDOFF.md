# Human Review Handoff

Use this file as the shortest manual review path before the final VnExpress Sáng kiến Khoa học 2026 submission.

## What Is Already Ready

- end-to-end MVP story is documented in `docs/contest/SUBMISSION_PACKAGE.md`
- smoke-backed validation is recorded in `docs/contest/VALIDATION_REPORT.md`
- screenshot evidence is current in `docs/contest/screenshots/`
- AI-verifiable submission items are checked in `ai_first/competition/submission-checklist.md`
- supporting contest text exists in:
  - `ai_first/competition/product-description.md`
  - `ai_first/competition/fork-modifications.md`
  - `ai_first/competition/pitch-notes.md`

## Remaining Human-Owned Decisions

### 1. Product description review

Confirm wording, claim calibration, and category fit for Education using:

- `ai_first/competition/product-description.md`
- `ai_first/competition/pitch-notes.md`
- `ai_first/competition/vnexpress-rules-summary.md`

### 2. Intellectual property commitment

Review the contest IP commitment outside the repository submission flow and confirm the maintained facts still match:

- Apache 2.0 license retained in `LICENSE`
- upstream attribution retained in `README.md` and `AGENTS.md`
- contest-specific fork modifications summarized in `ai_first/competition/fork-modifications.md`

### 3. Evidence sanity check

Before submission, quickly verify:

- screenshots are clear and contain no private data
- `docs/contest/VALIDATION_REPORT.md` still matches the intended demo environment
- optional video is either not required or has been recorded separately using `docs/contest/VIDEO_CAPTURE_RUNBOOK.md`

### 4. Final package sign-off

Use `docs/contest/SUBMISSION_PACKAGE.md` as the final read path and then mark the remaining human checklist items in the actual submission workflow.

## Suggested Human Read Order

1. `docs/contest/SUBMISSION_PACKAGE.md`
2. `ai_first/competition/submission-checklist.md`
3. `ai_first/competition/product-description.md`
4. `ai_first/competition/fork-modifications.md`
5. `docs/contest/VALIDATION_REPORT.md`
6. `docs/contest/screenshots/`

## Expected End State

After human review, the only repo state change that may still be useful is marking the final manual submission/sign-off outcome if the team wants a last archival docs sync.
