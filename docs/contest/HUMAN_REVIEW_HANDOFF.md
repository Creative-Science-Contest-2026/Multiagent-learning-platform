# Human Review Handoff

Use this file as the shortest manual review path before the final VnExpress Sáng kiến Khoa học 2026 submission.

## What Is Already Ready

- the official product loop and claim contract are documented in `docs/contest/SUBMISSION_PACKAGE.md`
- smoke-backed validation is recorded in `docs/contest/VALIDATION_REPORT.md`
- screenshot evidence is current in `docs/contest/screenshots/`
- AI-verifiable submission items are tracked in `ai_first/competition/submission-checklist.md`
- supporting contest text exists in `ai_first/competition/product-description.md`, `ai_first/competition/fork-modifications.md`, and `ai_first/competition/pitch-notes.md`

## Human Review Gates

### Gate 1. Product wording and category fit

Status: pending human review
Owner: submission operator / final reviewer

Confirm wording, claim calibration, and category fit for Education using:

- `ai_first/competition/product-description.md`
- `ai_first/competition/pitch-notes.md`
- `ai_first/competition/vnexpress-rules-summary.md`

Acceptance rule:

- keep the product framed as a teacher-controlled adaptive tutoring prototype
- keep the official loop at `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`
- reject any wording that implies school-scale deployment or autonomous final judgment

### Gate 2. Intellectual property commitment

Status: pending human confirmation
Owner: submission operator / project owner

Review the contest IP commitment outside the repository submission flow and confirm the maintained facts still match:

- Apache 2.0 license retained in `LICENSE`
- upstream attribution retained in `README.md` and `AGENTS.md`
- contest-specific fork modifications summarized in `ai_first/competition/fork-modifications.md`

### Gate 3. Evidence sanity check

Status: pending final manual pass
Owner: submission operator

Before submission, quickly verify:

- screenshots are clear and contain no private data
- `docs/contest/VALIDATION_REPORT.md` still matches the intended demo environment
- hybrid authoring claims stay calibrated: `/agents` authoring can be shown, and bounded automated proof now exists for the unified Tutor turn path; do not rewrite that as universal live binding across every entry point
- pilot or external-feedback language stays honest: use [`PILOT_STATUS.md`](./PILOT_STATUS.md) and keep `/api/v1/system/pilot-feedback-status` aligned with any real stored feedback instead of implying classroom validation that the repository does not contain
- optional video is either not required or has been recorded separately using `docs/contest/VIDEO_CAPTURE_RUNBOOK.md`

Acceptance rule:

- if Session B refreshes validation or evidence wording, use its files as authoritative
- if a screenshot or validation artifact is stale, do not silently mark the package ready

### Gate 4. Optional video decision

Status: pending human decision
Owner: submission operator

Decide one of:

- no video is required for the submission path
- video is required and will be recorded outside the repository using `docs/contest/VIDEO_CAPTURE_RUNBOOK.md`

### Gate 5. Final package sign-off

Status: pending after Gates 1-4
Owner: final reviewer

Use `docs/contest/SUBMISSION_PACKAGE.md` as the final read path and then mark the remaining human checklist items in the actual submission workflow.

## Suggested Human Read Order

1. `docs/contest/SUBMISSION_PACKAGE.md`
2. `ai_first/competition/submission-checklist.md`
3. `ai_first/competition/product-description.md`
4. `ai_first/competition/fork-modifications.md`
5. `docs/contest/VALIDATION_REPORT.md`
6. `docs/contest/screenshots/`

## Expected End State

After human review, the repo should have one visible answer for three questions:

- what the product claims
- what evidence supports those claims
- which manual gates were still human-only at sign-off
