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

- Owner: Coordination lane
- Machine:
- Worktree: `.worktrees/submission-close-master`
- Task: `OPS_SUBMISSION_CLOSE_MASTER`
- Status: in-review
- Branch: `docs/submission-close-master`
- Task packet: `docs/superpowers/tasks/2026-04-28-submission-close-master-coordination.md`
- Owned files: submission-close spec, plan, task packets, and AI-first mirrors
- PR: `#210`
- Last update: 2026-04-28
- Next action: monitor Draft PR `#210`, merge it when CI is green, then launch Session A, Session B, and Session C from fresh worktrees off `main`
- Blocker: current `main` no longer has the pytest collection mismatch, but the full baseline suite still contains post-collection failures outside this docs-planning lane

### Planned Assignment

- Owner: Session A
- Machine:
- Worktree: `.worktrees/submission-close-a`
- Task: `OPS_SUBMISSION_CLOSE_A`
- Status: planned
- Branch: `docs/submission-close-session-a`
- Task packet: `docs/superpowers/tasks/2026-04-28-session-a-submission-scope-and-narrative.md`
- Owned files: submission narrative and package docs
- PR:
- Last update: 2026-04-28
- Next action: start `PR-CLOSE-01`
- Blocker:

### Assignment

- Owner: Session B
- Machine: local
- Worktree: `.worktrees/submission-close-b`
- Task: `OPS_SUBMISSION_CLOSE_B`
- Status: in-review
- Branch: `docs/submission-close-session-b`
- Task packet: `docs/superpowers/tasks/2026-04-28-session-b-validation-and-evidence.md`
- Owned files: validation, smoke, demo-data, and evidence docs
- PR: `#212`
- Last update: 2026-04-28
- Next action: keep Draft PR `#212` green, then move it to Ready after self-review
- Blocker:

### Planned Assignment

- Owner: Session C
- Machine:
- Worktree: `.worktrees/submission-close-c`
- Task: `OPS_SUBMISSION_CLOSE_C`
- Status: planned
- Branch: `fix/submission-close-session-c`
- Task packet: `docs/superpowers/tasks/2026-04-28-session-c-runtime-fix-and-polish.md`
- Owned files: runtime fixes and optional polish only
- PR:
- Last update: 2026-04-28
- Next action: remain on standby until blocker fix or Phase 2 approval
- Blocker:
