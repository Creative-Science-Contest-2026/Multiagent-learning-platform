## Feature Pod Task: Runtime Task Depth Contract

Task ID: `OPS_RUNTIME_BRAINSTORMING_GATE`
Commit tag: `OPS_RUNTIME_BRAINSTORMING_GATE`
Owner: AI-first operating lane
Branch: `docs/runtime-task-depth-contract`
GitHub Issue:
Active assignment:

## Goal

Tighten the AI-first runtime-task contract so workers must inspect the broader code path before implementation instead of stopping after a shallow local fix.

## User-visible outcome

- Runtime tasks must read the brainstorming skill before implementation.
- Runtime tasks must declare a bounded design artifact, required code reading, and expected impact surface before editing code.
- Runtime tasks cannot claim completion without showing that sibling paths and validation paths were inspected.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/templates/feature-pod-task.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-runtime-task-depth-contract.md`
- `docs/superpowers/pr-notes/2026-04-30-runtime-task-depth-contract.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `.github/workflows/`
- `requirements/`
- `docs/package-lock.json`
- `web/package-lock.json`
- `.env*`
- committed `data/` files

## Output contract

- Keep the change bounded to AI-first operating docs and templates.
- Do not change runtime product code.
- Do not change unrelated dirty files in the current worktree.

## Validation

- `rg -n "Runtime-change design gate|codebase survey|impact surface|Required code reading|Impact surface and stop conditions" ai_first/AI_OPERATING_PROMPT.md ai_first/templates/feature-pod-task.md ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-runtime-task-depth-contract.md docs/superpowers/pr-notes/2026-04-30-runtime-task-depth-contract.md`
- `git diff --check -- ai_first/AI_OPERATING_PROMPT.md ai_first/templates/feature-pod-task.md ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-runtime-task-depth-contract.md docs/superpowers/pr-notes/2026-04-30-runtime-task-depth-contract.md`
