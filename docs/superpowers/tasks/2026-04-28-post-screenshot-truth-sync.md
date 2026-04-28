# Feature Pod Task: Post-Screenshot Truth Sync

Task ID: `OPS_SCREENSHOT_TRUTH_SYNC`
Commit tag: `OPS-SHOT-TRUTH`
Owner: Docs sync lane
Branch: `docs/post-screenshot-truth-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Repair the AI-first control-plane mirrors so they match the authoritative contest evidence docs on `main`, which still mark browser-backed Knowledge, Tutor, Dashboard, and `/agents` screenshots as stale after the Phase 2 polish merges.

## User-visible outcome

- `ai_first/AI_OPERATING_PROMPT.md` and compact mirrors stop claiming current browser screenshot freshness.
- The repo-level status clearly distinguishes `Current` command-backed validation from `Stale` browser screenshot rows.
- Future workers are pointed at the correct next AI-owned follow-up: a fresh browser recapture packet or execution lane, not a false terminal state.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-post-screenshot-truth-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-screenshot-truth-sync.md`

## Do-not-touch files/modules

- `docs/contest/*`
- `ai_first/TASK_REGISTRY.json`
- `web/`
- `deeptutor/`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- The mirrors explicitly reflect that command-backed evidence is current on 2026-04-28 while browser screenshot rows remain stale until recaptured.
- The mirrors do not describe browser screenshot freshness as current.
- The lane is documented with a bounded task packet and PR note only; no runtime or contest evidence files are changed.

## Required tests

- `rg -n "stale|browser screenshot|command-backed|Current|recapture|OPS_SCREENSHOT_TRUTH_SYNC" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.
