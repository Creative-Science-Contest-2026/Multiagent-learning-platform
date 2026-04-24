# Feature Pod Task: Contest Product Description Draft

Owner: Codex
Branch: `docs/t040-product-description`
GitHub Issue: `#104`

## Goal

Draft the contest product description from current MVP evidence and pitch materials so the submission package contains actual product-description text instead of an empty checklist slot.

## User-visible outcome

- A reusable contest product description draft exists in the repository.
- The submission checklist can mark `Product description drafted`.
- Submission docs move one step closer to purely human approval items.

## Owned files/modules

- `ai_first/competition/product-description.md`
- `ai_first/competition/submission-checklist.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-25-T040-contest-product-description.md`
- `docs/superpowers/pr-notes/` for the PR note
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-25.md`

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- `ai_first/competition/product-description.md` exists and is submission-ready as a draft.
- Submission checklist marks product description drafted.
- Submission package links to the new draft.
- Control-plane mirrors `T039` complete and `T040` active.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T040|product description|Partially verified|#103|#104" ai_first/competition docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
