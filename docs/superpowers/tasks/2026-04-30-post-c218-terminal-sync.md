## Feature Pod Task: Post-C218 Terminal Sync

Task ID: `OPS_POST_C218_SYNC`
Commit tag: `OPS-C218-SYNC`
Owner: Control-plane repair lane
Branch: `docs/c218-terminal-sync`
GitHub Issue:
Active assignment:

## Goal

Sync the AI-first control-plane mirrors after PR `#239` merged so `C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY` is recorded as completed and the repository no longer advertises a stale active wording lane.

## User-visible outcome

- `ai_first/TASK_REGISTRY.json` records `C218` as completed with the merged result.
- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer shows the merged `C218` lane as active.
- The compact mirrors point the next worker at `C219` or the browser-recapture follow-up instead of the already-merged terminology pass.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-30-post-c218-terminal-sync.md`
- `docs/superpowers/pr-notes/2026-04-30-post-c218-terminal-sync.md`
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
- Do not widen this lane into `C219`, screenshot recapture, or any runtime/product change.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY|C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD|#239|None\\." ai_first/AI_OPERATING_PROMPT.md ai_first/EXECUTION_QUEUE.md ai_first/NEXT_ACTIONS.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-post-c218-terminal-sync.md docs/superpowers/pr-notes/2026-04-30-post-c218-terminal-sync.md`
- `git diff --check`
