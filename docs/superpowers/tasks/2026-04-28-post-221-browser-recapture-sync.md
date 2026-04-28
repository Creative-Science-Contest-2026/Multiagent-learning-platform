# Feature Pod Task: Post-221 Browser Recapture Sync

Task ID: `OPS_POST_221_BROWSER_RECAPTURE_SYNC`
Commit tag: `OPS-221-SYNC`
Owner: Docs sync lane
Branch: `docs/post-221-browser-recapture-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Sync the authoritative AI-first control plane and compact mirrors after PR `#221` merged the post-Phase-2 browser screenshot recapture to `main`.

## User-visible outcome

- `ai_first/AI_OPERATING_PROMPT.md` and the compact mirrors agree that browser screenshot freshness is current again.
- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer shows the browser recapture lane as active.
- The repository returns to a clean terminal state: human review, optional video, or a newly opened packet from `main`.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-post-221-browser-recapture-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-221-browser-recapture-sync.md`

## Do-not-touch files/modules

- `docs/contest/screenshots/*`
- `docs/contest/*.md`
- `web/`
- `deeptutor/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- Prompt and mirrors mention PR `#221` as merged.
- No active browser recapture blocker remains in the queue.
- Human-review-only terminal state is clear from the prompt and compact mirrors.

## Required tests

- `rg -n "#221|browser recapture|human review|optional video|OPS_POST_221_BROWSER_RECAPTURE_SYNC" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.
