# 2026-04-28 C215 Post-Polish Evidence Recapture

- Task ID: `C215_POST_POLISH_EVIDENCE_RECAPTURE`
- Commit tag: `C215`
- Branch: `fix/submission-close-c215`
- Worktree: `.worktrees/submission-close-c`
- Status: `in-progress`

## Goal

Bring contest evidence docs back in sync with the current merged UI by separating current command-backed proof from stale browser screenshots after Phase 2 polish.

## Owned files

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `docs/contest/SUBMISSION_PACKAGE.md`
- `ai_first/evidence/screenshots.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/specs/2026-04-28-c215-post-polish-evidence-recapture-design.md`
- `docs/superpowers/plans/2026-04-28-c215-post-polish-evidence-recapture.md`
- `docs/superpowers/pr-notes/2026-04-28-c215-post-polish-evidence-recapture.md`

## Do-not-touch

- Screenshot files and video artifacts
- Machine-readable command-evidence artifact values
- Runtime/frontend code

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `rg -n "Stale|Current|post-polish|browser screenshots|recapture|#214|#215|#216" docs/contest ai_first/evidence docs/superpowers/tasks docs/superpowers/pr-notes`
- `git diff --check`

## Handoff

- Command-backed smoke evidence remains current from 2026-04-28.
- Browser screenshots for Knowledge, Tutor, Dashboard, and `/agents` are now explicitly marked stale until a fresh recapture pass happens against the current merged UI.
