# Feature Pod Task: Post-130 Screenshot Merge Sync

Owner: Codex
Branch: `docs/post-130-screenshot-sync`

## Goal

Sync the control-plane mirrors and contest entry docs after PR `#130` merged so the repository no longer reports the screenshot-refresh lane as active.

## Owned files/modules

- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-25.md`
- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-25-post-130-screenshot-sync.md`
- `docs/superpowers/pr-notes/` for the post-merge sync PR note

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/screenshots/*`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- No active assignment remains for the merged screenshot lane.
- Queue and prompt no longer describe the screenshot-refresh lane as still active.
- Contest entry docs reference the 2026-04-25 screenshot refresh instead of the older 2026-04-24 wording.
- PR note includes a Mermaid diagram and states whether `MAIN_SYSTEM_MAP.md` changed.

## Required tests

- `rg -n "2026-04-24|#130|screenshot refresh|active docs lane" ai_first docs/contest docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`
