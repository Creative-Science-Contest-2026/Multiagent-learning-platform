## Feature Pod Task: Active Assignments Policy Fix

Task ID: `OPS_ACTIVE_ASSIGNMENTS_POLICY_FIX`
Commit tag: `OPS-ACTIVE-POLICY`
Owner: Docs policy lane
Branch: `docs/active-assignments-policy-fix`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Stop the infinite post-merge sync loop by redefining `ai_first/ACTIVE_ASSIGNMENTS.md` as a board for live lanes only, with merged history preserved in the daily log and packet/PR-note trail instead of the active board itself. Docs-only terminal-state repair lanes are explicitly excluded from the board because their sole purpose is to mutate that board.

## User-visible outcome

- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer carries merged lanes that can become stale after every terminal sync PR.
- Docs-only terminal-state repair lanes no longer need to claim a slot in `ai_first/ACTIVE_ASSIGNMENTS.md`.
- `ai_first/AI_OPERATING_PROMPT.md` explicitly states that merged lanes must be removed from the active board after merge.
- The repo returns to a stable terminal state without requiring endless post-merge repair packets.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-active-assignments-policy-fix.md`
- `docs/superpowers/pr-notes/2026-04-28-active-assignments-policy-fix.md`

## Do-not-touch files/modules

- `ai_first/TASK_REGISTRY.json`
- `docs/contest/*`
- `web/`
- `deeptutor/`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`

## Acceptance criteria

- `ai_first/ACTIVE_ASSIGNMENTS.md` contains only live non-terminal lanes or an explicit `no active lanes` terminal state.
- The operating prompt states that merged lanes leave the active board and stay discoverable through daily logs and task/PR notes.
- The repair remains docs-only and does not reopen runtime, evidence, or submission narrative scope.

## Required tests

- `rg -n "live lanes|merged lanes|ACTIVE_ASSIGNMENTS|no active lanes|OPS_ACTIVE_ASSIGNMENTS_POLICY_FIX" ai_first/AI_OPERATING_PROMPT.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/CURRENT_STATE.md ai_first/daily/2026-04-28.md docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`
