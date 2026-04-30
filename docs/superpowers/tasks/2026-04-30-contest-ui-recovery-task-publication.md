# 2026-04-30 Contest UI Recovery Task Publication

- Task ID: `OPS_CONTEST_UI_RECOVERY_TASKS`
- Commit tag: `OPS-UI-RECOVERY`
- Branch: `docs/contest-ui-i18n-audit-tasks`
- Worktree: `.worktrees/contest-ui-i18n-audit-tasks`
- Status: `in_progress`

## Goal

Re-audit the current contest-facing runtime after `C216-C219` and publish new bounded follow-up packets if visible layout breakage or incomplete Vietnamese coverage still remain.

## Owned files

- `ai_first/TASK_REGISTRY.json`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-contest-ui-recovery-task-publication.md`
- `docs/superpowers/tasks/2026-04-30-c220-contest-layout-breakage-sweep.md`
- `docs/superpowers/tasks/2026-04-30-c221-contest-vietnamese-coverage-completion.md`
- `docs/superpowers/pr-notes/2026-04-30-contest-ui-recovery-task-publication.md`

## Do-not-touch

- runtime source files under `web/` and `deeptutor/`
- contest docs under `docs/contest/`
- lockfiles and generated files

## Execution notes

- This is a docs/control-plane lane only.
- Use the latest contest screenshots plus code inspection to justify any new task publication.
- Open only bounded follow-up packets that can be executed from `main` without colliding with each other.

## Acceptance criteria

- The registry records the newly discovered follow-up tasks.
- Each new task has its own execution packet.
- The control-plane mirrors stop claiming the repo is back to a purely human-only end state while these blockers remain open.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "C220_|C221_|layout breakage|Vietnamese coverage" ai_first/TASK_REGISTRY.json ai_first/AI_OPERATING_PROMPT.md ai_first/EXECUTION_QUEUE.md ai_first/NEXT_ACTIONS.md docs/superpowers/tasks -S`
- `git diff --check`
