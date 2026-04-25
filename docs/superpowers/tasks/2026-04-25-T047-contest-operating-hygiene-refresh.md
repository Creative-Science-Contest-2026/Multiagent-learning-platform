# Feature Pod Task: Contest Flow Operating Hygiene Refresh

Owner: Codex
Branch: `docs/t044-two-lane-parallel-backlog`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Refresh stale coordination docs so the repo can start a two-lane contest MVP polish experiment with accurate state, branch references, and ownership guidance.

## User-visible outcome

- The queue no longer claims the repo is only waiting on human review.
- The assignment board no longer shows stale merged work.
- Future workers can see the two-lane experiment before starting code.

## Owned files/modules

- `ai_first/TASK_REGISTRY.json`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-25.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `docs/contest/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## API/data contract

No runtime API or data contract changes.

## Acceptance criteria

- `T044` through `T051` exist in `ai_first/TASK_REGISTRY.json`.
- `T047` and `T048` are the active bootstrap tasks.
- The assignment board reflects the current backlog-rollout branch.
- Queue and snapshots point to the two-lane experiment.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T044|T045|T046|T047|T048|T049|T050|T051|two-lane|docs/t044-two-lane-parallel-backlog" ai_first docs/superpowers -S`
- `git diff --check`

## Manual verification

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` contains no stale `#119` entry.
- Confirm `ai_first/EXECUTION_QUEUE.md` names the two-lane experiment as active.

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- Keep this slice docs-only and bounded to the control plane.
- Do not start Lane 1 or Lane 2 implementation until this bootstrap packet is current.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not updated because this is control-plane only.

## Handoff notes
