# Feature Pod Task: Contest Smoke With Scripted Demo Reset

Owner: Documentation / Workflow AI worker
Branch: `docs/contest-smoke-scripted-reset`
GitHub Issue: `#37`

## Goal

Run the contest smoke lane using the scripted local demo data reset utility so the MVP evidence path proves the reset command works before future demo or submission work.

## User-visible outcome

A human or AI worker can read one execution packet, run the reset command, run the smoke lane, and know whether to refresh evidence docs or create the next focused bug task.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-19-contest-smoke-scripted-reset.md`
- `docs/superpowers/pr-notes/contest-smoke-scripted-reset-packet.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md` only if screenshot or video status changes
- `docs/contest/SMOKE_RUNBOOK.md` only if the smoke procedure needs a correction
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if repo-level status or next actions change

## Do-not-touch files/modules

- `deeptutor/` product/runtime code in this task-packet PR
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `web/next-env.d.ts`
- `.env*`
- committed `data/` files or private local data

## Execution contract

The smoke execution worker must:

1. start from a clean branch `docs/contest-smoke-scripted-reset`;
2. run `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`;
3. keep generated local `data/` changes out of commits;
4. run the smoke lane in `docs/contest/SMOKE_RUNBOOK.md` from Stage 1 through Stage 6;
5. stop on the first hard failure;
6. record commands, pass/fail result, and blocker details in `ai_first/daily/2026-04-19.md`;
7. update `docs/contest/VALIDATION_REPORT.md` only if smoke passes;
8. update `docs/contest/EVIDENCE_CHECKLIST.md` only if screenshot or video freshness changes;
9. create or update the next focused bug/task if smoke fails.

## Acceptance criteria

- The reset command is run before smoke.
- Smoke result is recorded with concrete commands and dates.
- Evidence docs are refreshed only after a successful smoke pass.
- Failure handling points to one next focused task instead of vague follow-up work.
- The PR includes an architecture note with Mermaid.

## Required validation

- `rg -n "scripted|reset|smoke|evidence|Knowledge Pack|contest|Mermaid" docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

## Manual verification for execution PR

- Confirm the reset command reports `contest-demo-quadratics`, `contest-assessment-demo`, and `contest-tutor-demo`.
- Confirm backend, frontend, Knowledge Pack, assessment, tutor, and dashboard stages pass or stop on the first hard failure.
- Confirm no generated local `data/` files are committed.

## PR architecture note

- Must include Mermaid diagram.
- State whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed. This packet PR should not need a map update because it queues a smoke execution workflow, not product/runtime architecture.

## Handoff notes

- The immediate next worker should implement this packet, not invent another queue lane.
- If local dependencies or environment setup block smoke, record the blocker clearly and leave evidence docs unchanged.
- Execution result: passed on 2026-04-19 with scripted reset, backend CLI server path, smoke API endpoints, and frontend production build.
- The backend `deeptutor.api.run_server` path still has a reload/absolute-pattern incompatibility with the installed `uvicorn`; smoke used `deeptutor_cli.main serve` with reload disabled.
