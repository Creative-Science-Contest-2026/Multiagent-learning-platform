# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#34`, which queued the scripted contest demo data reset utility.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules now live in `docs/contest/` on `main`.

## Active queue

- Open issue: `#35 feat: implement scripted contest demo data reset`
- Active task packet: `docs/superpowers/tasks/2026-04-19-scripted-demo-data-reset.md`
- Expected branch: `docs/scripted-demo-data-reset`

## Next recommended task

Land the scripted demo data reset utility, then use it before smoke/evidence refresh whenever local demo state may be stale.

## AI-owned blockers

- None currently. The local smoke lane passed with demo-safe data, backend startup, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed
