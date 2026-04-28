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

- Owner: Post-221 sync lane
- Machine: local
- Worktree: `.worktrees/submission-close-c`
- Task: `OPS_POST_221_BROWSER_RECAPTURE_SYNC`
- Status: review-ready
- Branch: `docs/post-221-browser-recapture-sync`
- Task packet: `docs/superpowers/tasks/2026-04-28-post-221-browser-recapture-sync.md`
- Owned files: authoritative prompt, compact mirrors, daily log, and sync PR note
- PR: `#222`
- Last update: 2026-04-28
- Next action: keep PR `#222` green and merge it once required checks pass
- Blocker: none

### Assignment

- Owner: Coordination lane
- Machine:
- Worktree: `.worktrees/submission-close-master`
- Task: `OPS_SUBMISSION_CLOSE_MASTER`
- Status: merged
- Branch: `docs/submission-close-master`
- Task packet: `docs/superpowers/tasks/2026-04-28-submission-close-master-coordination.md`
- Owned files: submission-close spec, plan, task packets, and AI-first mirrors
- PR: `#210`
- Last update: 2026-04-28
- Next action: preserve the merged coordination packet as the historical entrypoint for submission-close Phase 1
- Blocker: current `main` no longer has the pytest collection mismatch, but the full baseline suite still contains post-collection failures outside this docs-planning lane

### Assignment

- Owner: Session A
- Machine:
- Worktree: `.worktrees/submission-close-a`
- Task: `OPS_SUBMISSION_CLOSE_A`
- Status: merged
- Branch: `docs/submission-close-session-a`
- Task packet: `docs/superpowers/tasks/2026-04-28-session-a-submission-scope-and-narrative.md`
- Owned files: submission narrative and package docs
- PR: `#211`
- Last update: 2026-04-28
- Next action: keep the merged package docs as the current human-review path unless a Phase 2 polish packet is explicitly opened
- Blocker:

### Assignment

- Owner: Session B
- Machine: local
- Worktree: `.worktrees/submission-close-b`
- Task: `OPS_SUBMISSION_CLOSE_B`
- Status: merged
- Branch: `docs/submission-close-session-b`
- Task packet: `docs/superpowers/tasks/2026-04-28-session-b-validation-and-evidence.md`
- Owned files: validation, smoke, demo-data, and evidence docs
- PR: `#212`
- Last update: 2026-04-28
- Next action: keep the 2026-04-28 command-backed validation refresh as the authoritative proof baseline unless a later smoke pass replaces it
- Blocker:

### Assignment

- Owner: Session C
- Machine: local
- Worktree: `.worktrees/submission-close-c`
- Task: `C215_POST_POLISH_EVIDENCE_RECAPTURE`
- Status: merged
- Branch: `fix/submission-close-c215`
- Task packet: `docs/superpowers/tasks/2026-04-28-c215-post-polish-evidence-recapture.md`
- Owned files: evidence freshness docs plus required AI-first mirrors after the latest optional polish merges
- PR: `#217`
- Last update: 2026-04-28
- Next action: keep 2026-04-28 command-backed smoke evidence current, and treat browser screenshot recapture as a separate future packet if needed
- Blocker:

### Assignment

- Owner: Browser recapture execution lane
- Machine: local
- Worktree: `.worktrees/submission-close-c`
- Task: `OPS_BROWSER_RECAPTURE_AFTER_PHASE2`
- Status: merged
- Branch: `docs/post-phase2-browser-recapture-run`
- Task packet: `docs/superpowers/tasks/2026-04-28-browser-recapture-after-phase2.md`
- Owned files: browser screenshot artifacts, contest evidence docs, AI-first mirrors, daily log, and PR note for the recapture execution
- PR: `#221`
- Last update: 2026-04-28
- Next action: preserve the merged browser screenshot refresh as the current contest evidence baseline unless a later UI change makes these rows stale again
- Blocker: none
