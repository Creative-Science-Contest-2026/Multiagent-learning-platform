# Feature Pod Task: Scripted Contest Demo Data Reset

Owner: Documentation / Workflow AI worker
Branch: `docs/scripted-demo-data-reset`
GitHub Issue: `#35`

## Goal

Create a local, idempotent reset or seed utility for contest demo-safe data so smoke and evidence refresh runs can rebuild the MVP demo state without relying on pre-existing local `data/` contents.

## User-visible outcome

A human or AI worker can run one explicit local command to recreate the demo-safe Knowledge Pack and session evidence required by `docs/contest/DEMO_DATA_RESET.md`, then run the smoke lane against known data.

## Owned files/modules

- `scripts/contest/` or another explicit contest/demo script path chosen during implementation
- `tests/` for the reset utility if implementation adds Python code
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/contest/VALIDATION_REPORT.md`
- `docs/superpowers/pr-notes/scripted-demo-data-reset.md`
- `docs/superpowers/pr-notes/scripted-demo-data-reset-packet.md`
- `docs/superpowers/tasks/2026-04-19-scripted-demo-data-reset.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if operating guidance changes

## Do-not-touch files/modules

- `deeptutor/` product/runtime code unless the implementation proves a narrow reusable helper is required and updates this packet first
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `web/next-env.d.ts`
- `.env*`
- committed `data/` files or private local data

## Utility contract

The implementation should add a local-only command or script that:

1. creates or updates only demo-safe records;
2. is idempotent across repeated runs;
3. creates or verifies Knowledge Pack `contest-demo-quadratics`;
4. creates or verifies sessions `contest-assessment-demo` and `contest-tutor-demo`;
5. leaves enough dashboard activity for smoke checks to confirm assessment and tutor context;
6. prints the ids and paths it touched;
7. refuses to run against production, unknown remote URLs, or environments that look unsafe;
8. does not require real LLM credentials;
9. does not commit generated `data/` changes.

The utility should follow the manual contract in `docs/contest/DEMO_DATA_RESET.md` and update that runbook with the final command.

## Acceptance criteria

- One explicit local command can rebuild or verify the demo-safe dataset.
- The command can run repeatedly without duplicating or corrupting demo data.
- The implementation has focused tests for idempotency and safety gates when practical.
- Smoke docs point to the command before smoke execution.
- No secrets, credentials, or private student data are added.
- The PR includes an architecture note with Mermaid.

## Required validation

- `pytest tests/scripts/test_reset_demo_data.py -v`
- `rg -n "demo data|reset|seed|smoke|Knowledge Pack|contest|Mermaid" scripts tests docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

If implementation touches Python code, also run:

- `python3 -m compileall scripts deeptutor`

## Manual verification

- Run the reset command in a local demo environment.
- Confirm it reports the Knowledge Pack and session ids.
- Run `docs/contest/SMOKE_RUNBOOK.md`.
- Update `docs/contest/VALIDATION_REPORT.md` only after smoke passes.

## PR architecture note

- Must include Mermaid diagram.
- State whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed. It should not need a map update if the utility is a local docs/demo helper.

## Handoff notes

- Keep this utility local and demo-only.
- Prefer a small script with explicit file/API boundaries over broad product changes.
- If a script cannot safely be implemented without runtime changes, stop and update this packet before editing runtime code.
