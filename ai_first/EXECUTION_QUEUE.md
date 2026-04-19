# Execution Queue

Last updated: 2026-04-19

This is the compact status board for humans and AI workers.  
The authoritative control plane is still `ai_first/AI_OPERATING_PROMPT.md`.

## Latest merged result

- Latest merged PR before the current active branch: `#42`, which queued the contest submission package lane.
- Core MVP path is already in `main`: Knowledge Pack, Assessment Builder, Student Tutor context, Teacher Dashboard, contest evidence screenshots, and backend/frontend/docs CI.
- Smoke-backed evidence refresh rules, the local demo reset command, and the scripted-reset smoke result now live in `docs/contest/` on `main`.

## Active queue

- Open issue: `#41 docs: prepare contest submission package`
- Active task packet: `docs/superpowers/tasks/2026-04-19-contest-submission-package.md`
- Expected branch: `docs/contest-submission-package`

## Next recommended task

Merge the contest submission package when checks pass. After merge, the remaining near-term work is human review of IP commitment, final product description wording, and whether optional video is required.

## AI-owned blockers

- None currently. The scripted-reset smoke lane passed with demo-safe reset output, backend startup through the CLI server path, frontend production build, Knowledge Pack metadata, assessment session evidence, tutor session evidence, and dashboard activity.

## Human-review blockers

- None currently. Human review is still required for product direction changes, deployment or credential decisions, and any PR explicitly marked blocked.

## Read path

1. `ai_first/AI_OPERATING_PROMPT.md`
2. `ai_first/EXECUTION_QUEUE.md`
3. Task packet for the active branch
4. `ai_first/CURRENT_STATE.md` only if more context is needed
