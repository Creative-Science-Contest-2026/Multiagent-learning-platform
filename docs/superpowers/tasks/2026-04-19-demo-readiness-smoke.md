# Feature Pod Task: Demo Readiness Smoke Lane

Owner: Documentation / Workflow AI worker
Branch: `docs/demo-readiness-smoke`
GitHub Issue: `#22`

## Goal

Add a docs-first smoke lane that verifies the contest MVP demo path end to end and turns failures into the next task.

## User-visible outcome

A human or AI worker can run one compact smoke flow and know whether the contest MVP path is still alive.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-19-demo-readiness-smoke.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/superpowers/pr-notes/demo-readiness-smoke-packet.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if the queue or operating rules change

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `web/next-env.d.ts`
- `.env*`
- `data/`

## Smoke contract

The smoke lane must verify this path in order:

1. backend startup path works;
2. frontend startup or build path works;
3. Knowledge Pack metadata is available;
4. assessment generation works with Knowledge Pack context;
5. Tutor workspace answers with Knowledge Pack context;
6. Dashboard shows recent activity.

For each stage, the lane must define:

- the command or manual action;
- the expected success condition;
- whether failure stops the lane immediately;
- where to record the outcome.

If the smoke lane fails:

- product/runtime failures become the next task;
- environment or credential blockers must be recorded clearly in `ai_first/EXECUTION_QUEUE.md` and `ai_first/daily/2026-04-19.md`.

## Acceptance criteria

- There is one explicit smoke-lane task packet.
- The task packet points to one compact smoke execution doc.
- Pass/fail and blocker behavior are explicit.
- The task remains docs/workflow-only.

## Required validation

- `rg -n "smoke|demo readiness|Knowledge Pack|assessment|Tutor|Dashboard|Mermaid" docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

## Manual verification

- Open the smoke runbook without reading old chat history.
- Confirm a new AI worker can identify the smoke path and stop conditions.
- Confirm the runbook says what becomes the next task if smoke fails.

## PR architecture note

- Must include Mermaid diagram.
- State that `ai_first/architecture/MAIN_SYSTEM_MAP.md` does not need an update because this packet adds queue/reporting docs, not product/runtime architecture.

## Handoff notes

- Keep round 1 docs-first.
- Do not add deployment, staging, or CI smoke automation in this packet.
- Reuse existing contest evidence docs instead of creating another evidence tree.
