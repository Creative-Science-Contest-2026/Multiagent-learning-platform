## Feature Pod Task: Post-229 Active Assignments Merge Sync

Task ID: `OPS_POST_229_ACTIVE_ASSIGNMENTS_SYNC`
Commit tag: `OPS-POST-229`
Owner: Active-assignment merge sync lane
Branch: `docs/post-terminal-state-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Repair the active-assignment mirror after PR `#229` merged so `OPS_SCREENSHOT_TRUTH_SYNC` is no longer shown as `ready-for-review`.

## User-visible outcome

- `ai_first/ACTIVE_ASSIGNMENTS.md` reflects that `OPS_SCREENSHOT_TRUTH_SYNC` is merged.
- The daily log records the tiny terminal-state repair lane.
- No broader submission-close files are reopened.

## Owned files/modules

- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-post-229-active-assignments-merge-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-229-active-assignments-merge-sync.md`

## Do-not-touch files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/TASK_REGISTRY.json`
- `docs/contest/*`
- `web/`
- `deeptutor/`

## Acceptance criteria

- No stale `ready-for-review` state remains for merged PR `#229`.
- The repair stays bounded to active-assignment and daily-log truth only.

## Required tests

- `rg -n "OPS_SCREENSHOT_TRUTH_SYNC|OPS_POST_229_ACTIVE_ASSIGNMENTS_SYNC|#229|ready-for-review|merged" ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-28.md docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`
