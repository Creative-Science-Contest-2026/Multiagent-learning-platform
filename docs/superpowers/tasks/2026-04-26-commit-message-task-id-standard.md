# Feature Pod Task: Commit Message Task ID Standard

Task ID: `OPS_COMMIT_MESSAGE_STANDARD`
Commit tag: `OPS-COMMIT`
Owner: Session-specific
Branch: `docs/commit-message-task-id-standard`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Add one simple commit-message convention so every commit references the active task without forcing humans or AI workers to remember per-lane exceptions.

## User-visible outcome

- AI workers can read `ai_first/AI_OPERATING_PROMPT.md` and know how to format commits.
- Task packets expose the task identifier needed for commit messages.
- The six active lane packets already carry stable commit tags before new sessions start.

## Owned files/modules

- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/daily/2026-04-26.md`
- `docs/superpowers/tasks/README.md`
- `docs/superpowers/tasks/templates/feature-pod-task.md`
- `docs/superpowers/tasks/2026-04-26-commit-message-task-id-standard.md`
- `docs/superpowers/tasks/2026-04-26-lane-*.md`
- `docs/superpowers/pr-notes/2026-04-26-commit-message-task-id-standard.md`

## Do-not-touch files/modules

- Product or runtime source files outside the docs/workflow control plane
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` unless the operating docs unexpectedly change system structure

## API/data contract

- Commit format must be easy to apply in both human and AI workflows.
- The task packet becomes the first place to look for `Task ID` and `Commit tag`.
- Registry-backed work should keep using registry task IDs rather than inventing duplicates.

## Acceptance criteria

- `ai_first/AI_OPERATING_PROMPT.md` defines one canonical commit format with examples.
- The task packet template and task-packet README require `Task ID` and `Commit tag`.
- The six lane packets expose stable task identifiers for future sessions.
- The docs packet itself can be committed using the new convention.

## Required tests

- `rg -n "Commit message convention|Task ID|Commit tag|OPS-COMMIT|\\[L[1-6]\\]" ai_first docs/superpowers/tasks docs/superpowers/pr-notes -S`
- `git diff --check`

## Manual verification

- Open `ai_first/AI_OPERATING_PROMPT.md` and confirm the commit format is visible without reading other docs.
- Open any lane packet and confirm the task metadata appears before the goal section.
- Confirm the branch's own commit message uses `[OPS-COMMIT]`.

## Parallel-work notes

- Keep this change docs/workflow-only.
- If another session is already changing task packet headers or the operating prompt, ask the human to resolve overlap before editing.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` should remain unchanged because this is control-plane only.

## Handoff notes

- This packet exists so the commit-tagging rule can apply to its own rollout.
