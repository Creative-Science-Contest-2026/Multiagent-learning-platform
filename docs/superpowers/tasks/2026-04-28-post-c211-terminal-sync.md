# Feature Pod Task: Post-C211 Terminal Sync

Task ID: `OPS_POST_C211_TERMINAL_SYNC`
Commit tag: `OPS-C211-SYNC`
Owner: Docs sync lane
Branch: `docs/post-c211-terminal-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Sync the task registry and remaining AI-first mirrors after PR `#219` and the later browser-evidence/control-plane merges so `main` lands in one coherent terminal state.

## User-visible outcome

- `C211_TEACHER_FIRST_ENTRY_POLISH` is marked `completed` in `ai_first/TASK_REGISTRY.json`.
- The prompt, queue, and compact mirrors no longer describe optional Phase 2 or browser recapture as pending work.
- The repository ends in the correct wait state: human review, optional video, or a newly opened packet from `main`.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-post-c211-terminal-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-c211-terminal-sync.md`

## Do-not-touch files/modules

- `docs/contest/*`
- `docs/contest/screenshots/*`
- `web/`
- `deeptutor/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`
- Any runtime or evidence artifact files outside the mirrors above

## Acceptance criteria

- Registry marks `C211` completed with merged-PR notes.
- Active assignments no longer show any Phase 2 lane as active or review-ready.
- Prompt and queue describe the current state as human review plus optional video only.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C211|#219|#221|#222|human review|optional video|browser recapture|OPS_POST_C211_TERMINAL_SYNC" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.
