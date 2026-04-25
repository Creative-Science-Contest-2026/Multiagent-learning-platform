# Feature Pod Task: Contest Human Review Handoff

Owner: Codex
Branch: `docs/t042-human-review-handoff`
GitHub Issue: `#108`

## Goal

Package the remaining human-only submission work into a short read path so the contest queue ends in a clear waiting-on-human state instead of a stale active task.

## User-visible outcome

- A short human review handoff document exists in the repository.
- The submission package links directly to the manual review path.
- Control-plane mirrors `T041` complete and `T042` active.

## Owned files/modules

- `docs/contest/HUMAN_REVIEW_HANDOFF.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-25-T042-contest-human-review-handoff.md`
- `docs/superpowers/pr-notes/` for the PR note
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-25.md`

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/competition/submission-checklist.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- `docs/contest/HUMAN_REVIEW_HANDOFF.md` exists and lists the remaining manual submission actions.
- Submission package links to the new handoff doc.
- Control-plane mirrors `T041` complete and `T042` active.
- Queue language explicitly says the remaining blockers are human-owned.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T042|human review handoff|#107|#108|waiting on manual review|HUMAN_REVIEW_HANDOFF" docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
