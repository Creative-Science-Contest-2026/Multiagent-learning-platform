# Feature Pod Task: Contest Submission Package

Owner: Documentation / Workflow AI worker
Branch: `docs/contest-submission-package`
GitHub Issue: `#41`

## Goal

Create a compact contest submission package so a human or AI worker can review the MVP story, evidence, smoke status, screenshots, known limitations, and final submission checklist from one read path.

## User-visible outcome

The contest package should make it possible to open one Markdown entry point and answer:

1. what the product demo story is;
2. what evidence proves the MVP path works;
3. which screenshots and optional video artifacts are ready;
4. what known limitations or environment notes remain;
5. what still needs human review before submission.

## Owned files/modules

- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/contest/README.md`
- `ai_first/competition/submission-checklist.md`
- `ai_first/competition/pitch-notes.md` only if links or status need updating
- `docs/superpowers/tasks/2026-04-19-contest-submission-package.md`
- `docs/superpowers/pr-notes/contest-submission-package.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if repo-level status or next actions change

## Do-not-touch files/modules

- `deeptutor/` product/runtime code
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `web/next-env.d.ts`
- `.env*`
- committed `data/` files or private local data
- large video files

## Package contract

The package must link, not duplicate, the current authoritative materials:

1. demo story and submission narrative;
2. pitch notes and contest rules summary;
3. validation report and evidence checklist;
4. screenshot inventory;
5. scripted demo reset and smoke runbook;
6. latest scripted-reset smoke result;
7. known limitations and human-review items;
8. final submission checklist.

## Acceptance criteria

- One Markdown package entry point exists under `docs/contest/`.
- `docs/contest/README.md` links to the package.
- The package clearly marks what is ready, deferred, or needs human review.
- The package references the scripted-reset smoke result from PR `#40`.
- The PR includes an architecture note with Mermaid.

## Required validation

- `rg -n "submission|package|pitch|evidence|smoke|screenshot|video|Mermaid|contest" docs/contest ai_first/competition docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

## Manual verification

- Open `docs/contest/SUBMISSION_PACKAGE.md`.
- Confirm a new reviewer can follow the demo, evidence, validation, and remaining human-review items without reading old chat history.
- Confirm no private data, credentials, generated local data, or large video files were added.

## PR architecture note

- Must include Mermaid diagram.
- State whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed. This task should not need a map update because it is contest documentation packaging, not product/runtime architecture.

## Handoff notes

- Keep this package short and link-heavy.
- Do not recapture screenshots or video in this task unless the package reveals a clear gap.
- If optional video becomes required, create a separate focused capture task.
