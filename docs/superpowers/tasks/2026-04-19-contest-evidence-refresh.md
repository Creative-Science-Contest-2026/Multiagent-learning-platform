# Feature Pod Task: Contest Evidence Refresh

Owner: Documentation / Workflow AI worker
Branch: `docs/contest-evidence-refresh`
GitHub Issue: `#26`

## Goal

Add a compact docs/workflow lane for refreshing contest evidence after smoke runs so the evidence bundle stays aligned with the current MVP path.

## User-visible outcome

A human or AI worker can tell what evidence should be refreshed after a smoke pass, what can stay as-is, and where to record the latest evidence status without reading old chat history.

## Owned files/modules

- `docs/contest/README.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/superpowers/tasks/2026-04-19-contest-evidence-refresh.md`
- `docs/superpowers/pr-notes/contest-evidence-refresh-packet.md`
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

## Evidence refresh contract

The evidence refresh lane must define:

1. what evidence is refreshed automatically after a smoke pass;
2. what evidence still requires a human-triggered capture step;
3. how to mark evidence as current, stale, or blocked;
4. where the latest smoke-backed evidence status is recorded.

The lane must reuse the current contest evidence bundle and smoke runbook. It must not create a second evidence tree.

## Acceptance criteria

- There is one explicit evidence-refresh task packet.
- The packet points to the existing contest evidence bundle and smoke runbook.
- The queue and status mirrors point to evidence refresh as the next short task.
- The change stays docs/workflow-only.

## Required validation

- `rg -n "evidence refresh|smoke|validation|screenshot|video|Mermaid" docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

## Manual verification

- Open the packet and confirm a new AI worker can tell what evidence to refresh after a smoke pass.
- Confirm the packet does not introduce another evidence or queue system.

## PR architecture note

- Must include Mermaid diagram.
- State that `ai_first/architecture/MAIN_SYSTEM_MAP.md` does not need an update because this packet adds docs/workflow guidance, not product/runtime architecture.

## Handoff notes

- Keep this lane docs/workflow-only.
- Reuse `docs/contest/` and `ai_first/EXECUTION_QUEUE.md`.
- Prefer small, repeatable evidence updates over large manual refresh work.
