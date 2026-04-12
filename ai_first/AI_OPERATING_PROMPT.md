# AI Operating Prompt

You are working on an AI-first competition project built from HKUDS/DeepTutor under Apache 2.0.

## Mission

Build a stable VnExpress Sáng kiến Khoa học 2026 MVP:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Required startup sequence

Before edits:

1. Continue from the repo-level instructions in `AGENTS.md`.
2. Read `ai_first/CURRENT_STATE.md`.
3. Read `ai_first/NEXT_ACTIONS.md`.
4. Read the relevant spec, plan, or task packet.
5. Run `git status --short --branch`.

## Work rules

- Never push directly to `main`.
- Use a focused branch.
- Respect `Owned files/modules` and `Do-not-touch files/modules`.
- For bootstrap tasks before task packets exist, use the current plan task's `Files:` section as the owned-file contract.
- Do not revert user or other-agent changes.
- Do not remove Apache 2.0 license or upstream credit.
- Do not modify lockfiles unless dependency changes require it.
- Prefer small, reviewable commits.

## Architecture rules

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is the main system map.
- During bootstrap, create missing architecture and PR-note folders from the approved plan before requiring future PRs to use them.
- Every PR must include a PR architecture note in `docs/superpowers/pr-notes/`.
- Every PR architecture note must include a Mermaid diagram.
- Update `MAIN_SYSTEM_MAP.md` when adding, removing, or materially changing features, tools, capabilities, routers, routes, data models, or the AI-first workflow.

## Completion rules

Before handing off:

1. Run relevant tests.
2. Record tests and failures.
3. Update `ai_first/daily/YYYY-MM-DD.md`.
4. Update `CURRENT_STATE.md` or `NEXT_ACTIONS.md` if status changed.
5. Add handoff notes with changed files, risks, and next recommended read path.
