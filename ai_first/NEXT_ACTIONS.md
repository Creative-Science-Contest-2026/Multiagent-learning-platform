# Next Actions

Last updated: 2026-04-19

This file is a compatibility snapshot. The authoritative action list lives in `ai_first/AI_OPERATING_PROMPT.md`.

## Immediate

1. Audit the existing `pod-a/teacher-knowledge-pack-mvp` worktree before continuing implementation because it contains uncommitted cross-scope changes.
2. Complete Pod A: Teacher Knowledge Pack MVP from `docs/superpowers/tasks/2026-04-13-teacher-knowledge-pack-pod-a.md`.
3. Open a Pod A PR linked to GitHub issue `#2` with a PR architecture note and Mermaid diagram.
4. Fix any Pod A CI, test, or review blockers before starting the next feature.
5. After Pod A merges, start Pod B: Assessment Builder and Student Tutor Workspace MVP from `docs/superpowers/tasks/2026-04-13-assessment-student-workspace-pod-b.md`.
6. Keep GitHub issues `#2` and `#3` aligned with the task packets and implementation PRs.

## After Milestone 0

1. Add Teacher Dashboard MVP planning after Pod A ownership is stable.
2. Keep the main system map updated when shared contracts change.
3. Keep `ai_first/AI_FIRST_ROADMAP.md` current when the autonomous operating loop changes.
4. Add reliable backend and frontend CI checks before allowing broader runtime auto-merge.

## Human Review Needed

- Confirm whether Teacher Dashboard should stay in a later Pod A packet or be folded into the same implementation branch.
- Review product scope changes, credential/deployment decisions, or PRs marked blocked by the AI worker.

## Mirror Policy

Use this file only as a compact queue mirror. Do not rely on it for the full operating contract. For a human-friendly quick start, read `ai_first/USAGE_GUIDE.md`.
