# Feature Pod Task: Post-T043 Optional Video Wait-State Sync

Owner: Codex
Branch: `docs/t043-post-merge-sync`
GitHub Issue: `#114`

## Goal

Sync the control-plane after `T043` merged so the repository no longer shows an active optional-video lane when the contest package is again waiting on human review.

## User-visible outcome

- `T043` is marked completed in task tracking.
- The execution queue returns to a waiting-on-human-review state.
- Future AI workers can see that the next valid action is human review or actual video recording, not another docs lane by default.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-25.md`
- `docs/superpowers/tasks/2026-04-25-post-t043-optional-video-wait-state-sync.md`
- `docs/superpowers/pr-notes/` for the PR note

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VIDEO_CAPTURE_RUNBOOK.md`
- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `ai_first/competition/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- `T043` is marked completed in `ai_first/TASK_REGISTRY.json`.
- `ai_first/EXECUTION_QUEUE.md` says there is no active AI implementation task.
- `ai_first/AI_OPERATING_PROMPT.md` reflects the waiting-on-human-review state after the optional video runbook merge.
- Daily log records the `#113` merge completion.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T043|#113|#114|No active AI implementation task|VIDEO_CAPTURE_RUNBOOK|waiting on human review" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
