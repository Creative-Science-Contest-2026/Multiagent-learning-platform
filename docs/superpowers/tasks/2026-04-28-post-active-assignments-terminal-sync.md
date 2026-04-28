# Feature Pod Task: Post-Active-Assignments Terminal Sync

Task ID: `OPS_ACTIVE_ASSIGNMENTS_TERMINAL_SYNC`
Commit tag: `OPS-ACTIVE-SYNC`
Owner: Docs sync lane
Branch: `docs/post-active-assignments-terminal-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Remove the last control-plane contradiction on `main` by syncing `ai_first/ACTIVE_ASSIGNMENTS.md` with the already-merged terminal state from PR `#225`.

## User-visible outcome

- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer shows PR `#225` as `ready-for-review`.
- The active-assignment mirror agrees with `ai_first/AI_OPERATING_PROMPT.md` and `ai_first/EXECUTION_QUEUE.md` that submission-close has no active AI-owned blocker.
- The repo remains in terminal state: human review, optional video, or a newly opened packet from `main`.

## Owned files/modules

- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-post-active-assignments-terminal-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-active-assignments-terminal-sync.md`

## Do-not-touch files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `docs/contest/*`
- `web/`
- `deeptutor/`

## Acceptance criteria

- The `OPS_C211_REGISTRY_REPAIR` entry is recorded as merged with PR `#225`.
- No `ready-for-review` state remains for an already-merged lane.
- The new sync lane is documented with a bounded packet and PR note.

## Required tests

- `rg -n "OPS_ACTIVE_ASSIGNMENTS_TERMINAL_SYNC|OPS_C211_REGISTRY_REPAIR|#225|ready-for-review|merged" ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-28.md docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.
