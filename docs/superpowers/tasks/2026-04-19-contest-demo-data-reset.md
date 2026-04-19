# Feature Pod Task: Contest Demo Data Reset

Owner: Documentation / Workflow AI worker
Branch: `docs/contest-demo-data-reset`
GitHub Issue: `#29`

## Goal

Add a compact task packet for making the contest demo dataset reproducible so AI workers can rebuild the demo-safe state instead of depending on whatever local data already exists.

## User-visible outcome

A human or AI worker can tell what demo-safe data must exist for the contest MVP path, what must be recreated automatically versus checked manually, and where the reset procedure should live.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-19-contest-demo-data-reset.md`
- `docs/superpowers/pr-notes/contest-demo-data-reset-packet.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if the queue or operating guidance changes

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

## Demo reset contract

The packet must define:

1. the minimum demo-safe Knowledge Pack and session state required for the contest MVP path;
2. which parts of that state should later be reset by script or seed workflow;
3. which parts still require a manual verification step after reset;
4. where the future reset runbook or script should be recorded.

The lane must reuse the current contest evidence bundle, smoke runbook, and AI-first control plane. It must not invent a second queue or evidence system.

## Acceptance criteria

- There is one explicit task packet for contest demo data reset.
- The packet points to the existing contest demo flow and smoke/evidence docs.
- The queue and status mirrors point to demo data reset as the next short task.
- The change stays docs/workflow-only.

## Required validation

- `rg -n "demo data|reset|smoke|evidence|Mermaid|Knowledge Pack|contest" docs/superpowers/tasks docs/superpowers/pr-notes ai_first docs/contest`
- `git diff --check`

## Manual verification

- Open the packet and confirm a new AI worker can tell why reproducible demo data is the next lane.
- Confirm the packet does not create a second evidence, smoke, or queue system.

## PR architecture note

- Must include Mermaid diagram.
- State that `ai_first/architecture/MAIN_SYSTEM_MAP.md` does not need an update because this packet adds docs/workflow guidance, not product/runtime architecture.

## Handoff notes

- Keep this lane docs/workflow-only.
- Reuse `docs/contest/` and `ai_first/EXECUTION_QUEUE.md`.
- Target a future implementation lane that makes demo-safe state reproducible before another smoke/evidence cycle depends on it.
