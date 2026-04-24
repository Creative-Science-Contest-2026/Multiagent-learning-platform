# Feature Pod Task: Contest Fork Modifications Note

Owner: Codex
Branch: `docs/t041-fork-modifications`
GitHub Issue: `#106`

## Goal

Document the contest-specific fork modifications from current repo evidence so the submission checklist can mark `Fork modifications described` and leave only human-review items unresolved.

## User-visible outcome

- A reusable fork-modifications note exists in the repository.
- The submission checklist can mark `Fork modifications described`.
- Submission docs move one step closer to human-only approval gaps.

## Owned files/modules

- `ai_first/competition/fork-modifications.md`
- `ai_first/competition/submission-checklist.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-25-T041-contest-fork-modifications.md`
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

- `ai_first/competition/fork-modifications.md` exists and summarizes contest-specific fork changes.
- Submission checklist marks `Fork modifications described`.
- Submission package links to the new note.
- Control-plane mirrors `T040` complete and `T041` active.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T041|fork modifications|#105|#106|Partially verified" ai_first/competition docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
