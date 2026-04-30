# Feature Pod Task: <feature name>

Owner:
Branch:
GitHub Issue:
Active assignment:

## Goal

## User-visible outcome

## Owned files/modules

## Do-not-touch files/modules

## API/data contract

## Design before implementation

- Runtime behavior change: yes/no
- If no: state why this task is docs-only, mirror-only, or otherwise non-runtime.
- If yes: confirm `.github/skills/brainstorming/SKILL.md` was read before implementation.
- Current behavior:
- Intended behavior change:
- Candidate approach A:
- Candidate approach B:
- Chosen approach and reason:
- Concrete files/modules expected to change:
- Tests to add or update:

## Required code reading

- Entry points/handlers to inspect:
- Primary logic/service/use-case modules to inspect:
- Shared contracts/schemas/types to inspect:
- Adjacent or reused flows to inspect:
- Existing tests to inspect:
- Notes from codebase survey:

## Impact surface and stop conditions

- Expected affected areas:
- Files/modules likely to change:
- Files/modules that must be reviewed even if they may remain unchanged:
- Minimum validation paths before the task can stop:
- What would count as a shallow fix for this task:
- Conditions that must be checked before marking done:

## Acceptance criteria

## Required tests

## Manual verification

## Parallel-work notes

- Confirm `ai_first/ACTIVE_ASSIGNMENTS.md` is updated before code starts.
- If another session is active on the same machine, use a separate worktree and record its path in `ai_first/ACTIVE_ASSIGNMENTS.md`.
- Before new work on an active lane, run `git fetch origin main` and merge `origin/main` in that lane's own worktree when `main` has advanced.
- Keep owned files concrete; do not use broad labels like "frontend" or "backend".
- Update this packet before scope expands.

## PR architecture note

- Must include Mermaid diagram.
- Must update `ai_first/architecture/MAIN_SYSTEM_MAP.md` if feature structure changes.

## Handoff notes
