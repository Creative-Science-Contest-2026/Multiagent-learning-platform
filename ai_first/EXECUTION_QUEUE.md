# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#36`, which added the scripted contest demo data reset utility.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules and the local demo reset command now live in `docs/contest/` on `main`.

## Active queue

- Open issue: `#37 docs: run contest smoke with scripted demo reset`
- Active task packet: `docs/superpowers/tasks/2026-04-19-contest-smoke-scripted-reset.md`
- Expected branch: `docs/contest-smoke-scripted-reset`

## Next recommended task

Run the contest smoke lane after executing `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`, then refresh evidence docs or create a bug task from the first hard failure.

## AI-owned blockers

- None currently. The local smoke lane passed with demo-safe data, backend startup, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed
