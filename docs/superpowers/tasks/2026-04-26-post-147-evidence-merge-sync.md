# Feature Pod Task: Post-147 Evidence Merge Sync

Task ID: `OPS_POST_147_EVIDENCE_SYNC`
Commit tag: `OPS-SYNC`
Owner: Session-specific
Branch: `docs/post-147-evidence-merge-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Sync the compact AI-first control-plane mirrors after PR `#147` merged so the repository no longer points workers at the already-completed dashboard and `/agents` screenshot recapture lane.

## User-visible outcome

- `ai_first/EXECUTION_QUEUE.md` reflects that contest screenshot evidence is current.
- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer advertises the merged recapture lane as the next pending task.
- The next operational step is clearly framed as human review and optional video, not stale screenshot work.

## Owned files/modules

- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-26.md`
- `docs/superpowers/tasks/2026-04-26-post-147-evidence-merge-sync.md`
- `docs/superpowers/pr-notes/*`

## Do-not-touch files/modules

- `docs/contest/screenshots/*`
- `docs/contest/*.md`
- `deeptutor/`
- `web/`
- `ai_first/AI_OPERATING_PROMPT.md` unless the operating rules themselves changed

## Acceptance criteria

- Latest merged result points to PR `#147`.
- Queue no longer instructs workers to rerun the screenshot recapture packet.
- Remaining blockers are described as human-review or optional-video tasks only.

## Required tests

- `rg -n "#147|screenshot|human review|optional video|ACTIVE_ASSIGNMENTS|EXECUTION_QUEUE" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged.
