## Feature Pod Task: Post-C217 Terminal Sync

Task ID: `OPS_POST_C217_SYNC`
Commit tag: `OPS-C217-SYNC`
Owner: Control-plane repair lane
Branch: `docs/c217-terminal-sync`
GitHub Issue:
Active assignment:

## Goal

Sync the AI-first control-plane mirrors after PR `#237` merged so `C217_TEACHER_COCKPIT_DEFAULT_ENTRY` is recorded as completed and the repository no longer advertises a stale active lane.

## User-visible outcome

- `ai_first/TASK_REGISTRY.json` records `C217` as completed with the merged result.
- `ai_first/ACTIVE_ASSIGNMENTS.md` no longer shows the merged `C217` lane as active.
- The shortest queue mirrors point the next worker at `C218` and `C219` instead of older pre-differentiation follow-ups.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-30-post-c217-terminal-sync.md`
- `docs/superpowers/pr-notes/2026-04-30-post-c217-terminal-sync.md`
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
- Do not widen this lane into `C218`, `C219`, screenshot recapture, or any runtime/product change.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C217_TEACHER_COCKPIT_DEFAULT_ENTRY|C219_CLASSROOM_CASE_STUDY_AND_BOUNDED_METRIC_CARD|C218_CONTEST_BRAND_AND_CLASSROOM_TERMINOLOGY|#237|None\\." ai_first/AI_OPERATING_PROMPT.md ai_first/EXECUTION_QUEUE.md ai_first/NEXT_ACTIONS.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-post-c217-terminal-sync.md docs/superpowers/pr-notes/2026-04-30-post-c217-terminal-sync.md`
- `git diff --check`
