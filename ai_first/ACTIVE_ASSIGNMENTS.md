# Active Assignments

Use this file as the short-lived coordination board for active work.

Rules:

- Add an assignment before starting code work.
- One person should hold one active task at a time.
- Keep entries short and factual.
- Update the entry when blocked, paused, moved to review, or merged.

## Template

### Assignment

- Owner:
- Machine:
- Worktree:
- Task:
- Status:
- Branch:
- Task packet:
- Owned files:
- PR:
- Last update:
- Next action:
- Blocker:

## Active

### Assignment

- Owner: Session-specific
- Machine:
- Worktree: `.worktrees/fix-baseline-pytest-collection-blocker`
- Task: `OPS_PYTEST_COLLECTION_BLOCKER`
- Status: in-progress
- Branch: `fix/baseline-pytest-collection-blocker`
- Task packet: `docs/superpowers/tasks/2026-04-28-baseline-pytest-collection-blocker.md`
- Owned files: test package markers, task packet, PR note, active assignment, and daily log
- PR:
- Last update: 2026-04-28
- Next action: commit the collection-fix lane and use it to unblock merge work on other branches that currently stop at pytest collection
- Blocker: post-collection baseline remains at 23 failing tests on current `main`, but the import-mismatch collector blocker is resolved
