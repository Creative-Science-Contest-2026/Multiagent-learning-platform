# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#27`, which queued the contest evidence refresh packet.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules now live in `docs/contest/` on the current branch and are waiting to merge.

## Active queue

- Open issue: none currently.
- Active task packet: `docs/superpowers/tasks/2026-04-19-contest-evidence-refresh.md`
- Expected branch: `docs/evidence-refresh-run`

## Next recommended task

Merge the contest evidence refresh execution lane, then derive the next short task packet from the MVP goal.

## AI-owned blockers

- None currently. The local smoke lane passed with demo-safe data, backend startup, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed
