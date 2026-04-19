# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#38`, which queued the scripted-reset smoke execution lane.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules and the local demo reset command now live in `docs/contest/` on `main`.

## Active queue

- Open issue: `#37 docs: run contest smoke with scripted demo reset`
- Active task packet: `docs/superpowers/tasks/2026-04-19-contest-smoke-scripted-reset.md`
- Expected branch: `docs/contest-smoke-scripted-reset`

## Next recommended task

Merge the scripted-reset smoke execution result when checks pass. After merge, derive the next short contest task from the MVP goal, likely final submission packaging or optional demo video capture.

## AI-owned blockers

- None currently. The scripted-reset smoke lane passed with demo-safe reset output, backend startup through the CLI server path, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed
