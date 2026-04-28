## Feature Pod Task: C211 Registry Terminal Repair

Task ID: `OPS_C211_REGISTRY_REPAIR`
Commit tag: `OPS-C211-REGFIX`
Owner: Control-plane repair lane
Branch: `docs/post-submission-close-terminal-repair`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Repair the last stale submission-close control-plane record so `C211_TEACHER_FIRST_ENTRY_POLISH` is marked completed after PR `#219` merged.

## User-visible outcome

- `ai_first/TASK_REGISTRY.json` matches the merged `C211` state already reflected elsewhere in the control plane.
- Future workers do not see a false optional-polish task still `in-progress`.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-28-c211-registry-terminal-repair.md`
- `docs/superpowers/pr-notes/2026-04-28-c211-registry-terminal-repair.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`

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
- Do not widen this lane into another evidence, browser, or runtime pass.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C211_TEACHER_FIRST_ENTRY_POLISH|#219|completed|in-progress" ai_first/TASK_REGISTRY.json ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-28.md docs/superpowers/tasks/2026-04-28-c211-registry-terminal-repair.md docs/superpowers/pr-notes/2026-04-28-c211-registry-terminal-repair.md`
- `git diff --check`
