# Feature Pod Task: Post-118 Control-Plane Sync

Owner: Codex
Branch: `docs/task-registry-count-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Sync the AI-first control plane after PR `#118` merged so the queue, prompt, and compatibility snapshots reflect the current merged state instead of the older `#116` marker.

## User-visible outcome

- Future AI workers see PR `#118` as the latest merged workflow result.
- The queue and compatibility snapshots stay aligned with the actual repo state.
- The active assignment board shows the current docs sync, not the previous merged lane.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-25.md`
- `docs/superpowers/tasks/2026-04-25-post-118-control-plane-sync.md`
- `docs/superpowers/pr-notes/2026-04-25-post-118-control-plane-sync.md`

## Do-not-touch files/modules

- Product/runtime source files
- `ai_first/TASK_REGISTRY.json`
- `docs/contest/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## API/data contract

No runtime API or data contract changes.

## Acceptance criteria

- `ai_first/AI_OPERATING_PROMPT.md` names `#118` as the latest merged status sync.
- `ai_first/EXECUTION_QUEUE.md` names `#118` as the latest merged result.
- `ai_first/CURRENT_STATE.md` and `ai_first/NEXT_ACTIONS.md` no longer point at the old `docs/post-116-collab-sync` branch.
- `ai_first/ACTIVE_ASSIGNMENTS.md` reflects the current sync branch and status.

## Required tests

- `rg -n "#118|docs/task-registry-count-sync|Post-118|ACTIVE_ASSIGNMENTS|waiting on human review|No active AI implementation task" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Confirm the latest merged PR is `#118`.
- Confirm the workspace is on `docs/task-registry-count-sync`.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Keep owned files concrete; do not use broad labels like "frontend" or "backend".
- Update this packet before scope expands.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated because this is control-plane only.

## Handoff notes
