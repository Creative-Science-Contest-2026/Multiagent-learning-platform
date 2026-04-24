# Feature Pod Task: Contest Submission Package Freshness Sync

Owner: Codex
Branch: `docs/t038-submission-readiness-sync`
GitHub Issue: `#100`

## Goal

Sync the contest-facing entry docs with the latest 2026-04-24 smoke and screenshot evidence so reviewers do not land on stale submission-facing summaries.

## User-visible outcome

- `docs/contest/README.md` reflects the current smoke-backed validation date.
- `docs/contest/SUBMISSION_PACKAGE.md` points at the latest evidence lanes and current screenshot state.
- AI-first tracking reflects `T037` complete and `T038` active.

## Owned files/modules

- `docs/contest/README.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-24-T038-contest-submission-readiness-sync.md`
- `docs/superpowers/pr-notes/` for the PR note
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-24.md`

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VALIDATION_REPORT.md` and `docs/contest/EVIDENCE_CHECKLIST.md` unless a documentation inconsistency is discovered while syncing entry docs
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- Contest entry docs no longer mention the old 2026-04-19 validation window.
- Contest entry docs reflect that screenshot evidence is current again after `T037`.
- AI-first queue mirrors `T037` as complete and `T038` as the active short task.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "2026-04-24|T037|T038|Current|Deferred|#99|#100" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.

