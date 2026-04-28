# 2026-04-28 C214 Judge-Facing Visual Asset Polish

- Task ID: `C214_JUDGE_FACING_VISUAL_ASSET_POLISH`
- Commit tag: `C214`
- Branch: `fix/submission-close-c214`
- Worktree: `.worktrees/submission-close-c`
- Status: `in-progress`

## Goal

Clarify how judges should read the existing screenshot bundle by tightening caption language, visual order, and supporting evidence notes.

## Owned files

- `docs/contest/README.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/specs/2026-04-28-c214-judge-facing-visual-asset-polish-design.md`
- `docs/superpowers/plans/2026-04-28-c214-judge-facing-visual-asset-polish.md`
- `docs/superpowers/pr-notes/2026-04-28-c214-judge-facing-visual-asset-polish.md`

## Do-not-touch

- Screenshot image files
- Runtime/frontend code
- Validation command outputs
- Contest claim boundaries

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "judge-facing|Judge-facing caption|Recommended judge-view order|Recommended Judge Visual Order|teacher control|adaptive support" docs/contest ai_first/evidence docs/superpowers/tasks docs/superpowers/pr-notes`
- `git diff --check`

## Handoff

- The screenshot set is unchanged; only caption intent, visual order, and judge-facing explanation were tightened.
- Claims remain bounded to validated-prototype proof and existing evidence dates.
