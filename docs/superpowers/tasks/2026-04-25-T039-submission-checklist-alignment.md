# Feature Pod Task: Submission Checklist Evidence Alignment

Owner: Codex
Branch: `docs/t039-submission-checklist-sync`
GitHub Issue: `#102`

## Goal

Align the final contest submission checklist with the repo evidence that AI can verify directly, while leaving human-only submission items explicitly unchecked.

## User-visible outcome

- The final checklist distinguishes AI-verified items from human-only review items.
- Contest submission docs no longer understate repo-verifiable legal and evidence readiness.
- AI-first tracking reflects `T038` complete and `T039` active.

## Owned files/modules

- `ai_first/competition/submission-checklist.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `docs/superpowers/tasks/2026-04-25-T039-submission-checklist-alignment.md`
- `docs/superpowers/pr-notes/` for the PR note
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-25.md`

## Do-not-touch files/modules

- Product/runtime source files
- `docs/contest/VALIDATION_REPORT.md` and `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/architecture/MAIN_SYSTEM_MAP.md`

## Acceptance criteria

- `T038` is marked completed in control-plane tracking.
- Submission checklist marks only the items that have direct repo evidence.
- Human-only items remain clearly unchecked.
- Submission package points readers at the partially verified checklist state.

## Required tests

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "T039|Apache 2.0|HKUDS/DeepTutor|No secrets committed|Partially verified|#101|#102" ai_first/competition docs/contest ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Must state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
