## Feature Pod Task: Post-C219 Terminal Sync

Task ID: `OPS_POST_C219_SYNC`
Commit tag: `OPS-C219-SYNC`
Owner: Control-plane repair lane
Branch: `docs/c219-terminal-sync`
GitHub Issue:
Active assignment:

## Goal

Sync the AI-first control-plane mirrors after PR `#241` merged so `C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD` is recorded as completed and the repository no longer advertises any open contest-differentiation lane.

## User-visible outcome

- `ai_first/TASK_REGISTRY.json` records `C219` as completed with the merged result.
- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer shows the merged `C219` lane as active.
- The compact mirrors move from “remaining differentiation queue” back to human review plus optional browser-freshness follow-up.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-30-post-c219-terminal-sync.md`
- `docs/superpowers/pr-notes/2026-04-30-post-c219-terminal-sync.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `.env*`
- committed `data/` files

## Output contract

- Keep the repair bounded to control-plane metadata only.
- Do not widen this lane into screenshot recapture, final submission edits, or any runtime/product change.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD|#241|None\\.|browser freshness|final sign-off" ai_first/AI_OPERATING_PROMPT.md ai_first/EXECUTION_QUEUE.md ai_first/NEXT_ACTIONS.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-post-c219-terminal-sync.md docs/superpowers/pr-notes/2026-04-30-post-c219-terminal-sync.md`
- `git diff --check`
