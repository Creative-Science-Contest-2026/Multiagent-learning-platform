# Feature Pod Task: Post Submission-Close Control-Plane Sync

Task ID: `OPS_POST_SUBMISSION_CLOSE_SYNC`
Commit tag: `OPS-SUBMIT-SYNC`
Owner: Control-plane sync lane
Branch: `docs/post-submission-close-sync`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Sync the AI-first control plane after submission-close PRs `#210`, `#211`, and `#212` merged so future workers see the real terminal state instead of stale pre-merge queue instructions.

## User-visible outcome

- Submission-close Phase 1 status is reflected correctly in the registry and queue mirrors.
- Active assignments no longer show Session A and Session B as still waiting on review.
- The next recommended step is human review or explicitly approved optional polish, not replaying already merged work.

## Owned files/modules

- `docs/superpowers/tasks/2026-04-28-post-submission-close-sync.md`
- `docs/superpowers/pr-notes/2026-04-28-post-submission-close-sync.md`
- `ai_first/AI_OPERATING_PROMPT.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/CURRENT_STATE.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`

## Do-not-touch files/modules

- `deeptutor/`
- `web/`
- `.github/workflows/`
- `requirements/`
- `package-lock.json`
- `docs/package-lock.json`
- `web/package-lock.json`
- `.env*`
- committed `data/` files

## Output contract

- Keep the mirrors concise and factual.
- Do not reopen Session A or Session B as active work after their PRs merged.
- Preserve the distinction between current human-only submission work and optional AI-owned Phase 2 polish.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "submission-close|C201|C210|C211|human review|optional video" ai_first docs/superpowers/tasks/2026-04-28-post-submission-close-sync.md`
- `git diff --check`
