# Feature Pod Task: Optional Contest Video Capture Runbook

Owner: Codex
Branch: `docs/t043-video-capture`
GitHub Issue: `#112`

## Goal

Prepare a reusable optional video storyboard and recording runbook so the contest package can add a video artifact quickly if the final submission requires one.

## User-visible outcome

- A video capture runbook exists in the contest docs.
- Evidence and submission docs point to the runbook without claiming the video is already recorded.
- Control-plane mirrors `T042` complete and `T043` active.

## Owned files/modules

- `docs/contest/VIDEO_CAPTURE_RUNBOOK.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `docs/superpowers/tasks/2026-04-25-T043-optional-video-capture-runbook.md`
- `docs/superpowers/pr-notes/` for the PR note
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-25.md`

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VALIDATION_REPORT.md`
- `ai_first/competition/submission-checklist.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- `docs/contest/VIDEO_CAPTURE_RUNBOOK.md` exists with clip order and recording guidance.
- Evidence/submission docs link to the runbook.
- Optional video remains clearly deferred until actually recorded.
- Control-plane mirrors `T042` complete and `T043` active.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T043|VIDEO_CAPTURE_RUNBOOK|optional video|#111|#112" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
