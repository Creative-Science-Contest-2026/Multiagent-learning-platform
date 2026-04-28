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

- Owner: Post-229 active-assignment sync lane
- Machine: local
- Worktree: `.worktrees/post-terminal-state-sync`
- Task: `OPS_POST_229_ACTIVE_ASSIGNMENTS_SYNC`
- Status: ready-for-review
- Branch: `docs/post-terminal-state-sync`
- Task packet: `docs/superpowers/tasks/2026-04-28-post-229-active-assignments-merge-sync.md`
- Owned files: `ai_first/ACTIVE_ASSIGNMENTS.md`, daily log, and sync task/PR note only
- PR: `#230`
- Last update: 2026-04-28
- Next action: merge the docs-only post-229 repair PR once checks are clear and no blocking review remains
- Blocker: none

### Assignment

- Owner: Screenshot truth sync lane
- Machine: local
- Worktree: `.worktrees/post-screenshot-truth-sync`
- Task: `OPS_SCREENSHOT_TRUTH_SYNC`
- Status: merged
- Branch: `docs/post-screenshot-truth-sync`
- Task packet: `docs/superpowers/tasks/2026-04-28-post-screenshot-truth-sync.md`
- Owned files: authoritative prompt, compact mirrors, daily log, and sync task/PR note only
- PR: `#229`
- Last update: 2026-04-28
- Next action: preserve the merged screenshot-truth sync as the current control-plane baseline for stale browser-backed evidence rows
- Blocker: none

### Assignment

- Owner: Active-assignment terminal sync lane
- Machine: local
- Worktree: `.worktrees/post-active-assignments-terminal-sync`
- Task: `OPS_ACTIVE_ASSIGNMENTS_TERMINAL_SYNC`
- Status: merged
- Branch: `docs/post-active-assignments-terminal-sync`
- Task packet: `docs/superpowers/tasks/2026-04-28-post-active-assignments-terminal-sync.md`
- Owned files: `ai_first/ACTIVE_ASSIGNMENTS.md`, daily log, and sync task/PR note only
- PR: `#227`
- Last update: 2026-04-28
- Next action: preserve the merged `#227` active-assignment sync as part of the terminal-state baseline
- Blocker: none

### Assignment

- Owner: Control-plane repair lane
- Machine: local
- Worktree: `.worktrees/post-submission-close-sync`
- Task: `OPS_C211_REGISTRY_REPAIR`
- Status: merged
- Branch: `docs/post-submission-close-terminal-repair`
- Task packet: `docs/superpowers/tasks/2026-04-28-c211-registry-terminal-repair.md`
- Owned files: `TASK_REGISTRY.json`, active-assignment mirror, daily log, and repair PR note only
- PR: `#225`
- Last update: 2026-04-28
- Next action: preserve the merged registry repair as the terminal-state baseline for `C211`
- Blocker: none

### Assignment

- Owner: Post-221 sync lane
- Machine: local
- Worktree: `.worktrees/submission-close-c`
- Task: `OPS_POST_221_BROWSER_RECAPTURE_SYNC`
- Status: merged
- Branch: `docs/post-221-browser-recapture-sync`
- Task packet: `docs/superpowers/tasks/2026-04-28-post-221-browser-recapture-sync.md`
- Owned files: authoritative prompt, compact mirrors, daily log, and sync PR note
- PR: `#222`
- Last update: 2026-04-28
- Next action: preserve the merged post-`#221` control-plane sync as the current terminal-state baseline
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

### Active Assignment

- Owner: Session C211
- Machine: local
- Worktree: `.worktrees/submission-close-c211`
- Task: `C211_TEACHER_FIRST_ENTRY_POLISH`
- Status: merged
- Branch: `fix/submission-close-c211`
- Task packet: `docs/superpowers/tasks/2026-04-28-c211-teacher-first-entry-polish.md`
- Owned files: teacher-entry product surfaces plus required AI-first mirrors for C211 only
- PR: `#219`
- Last update: 2026-04-28
- Next action: preserve the merged teacher-first entry wording as the current baseline unless a later packet changes those surfaces
- Blocker:

### Assignment

- Owner: Browser recapture packet lane
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
