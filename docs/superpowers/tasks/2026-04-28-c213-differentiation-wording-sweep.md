# 2026-04-28 C213 Differentiation Wording Sweep

- Task ID: `C213_DIFFERENTIATION_WORDING_SWEEP`
- Commit tag: `C213`
- Branch: `fix/submission-close-c213`
- Worktree: `.worktrees/submission-close-c`
- Status: `in-progress`

## Goal

Align contest-facing product wording with the teacher-controlled adaptive tutor framing across the bounded UI surfaces already used in the submission flow.

## Owned files

- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/specs/2026-04-28-c213-differentiation-wording-sweep-design.md`
- `docs/superpowers/plans/2026-04-28-c213-differentiation-wording-sweep.md`
- `docs/superpowers/pr-notes/2026-04-28-c213-differentiation-wording-sweep.md`

## Do-not-touch

- Backend and runtime logic
- Contest submission package docs
- Screenshots, evidence inventory, and visual assets
- Lockfiles and generated files

## Execution notes

- Keep the sweep wording-only.
- Preserve existing layout and component structure.
- Prefer language that highlights teacher review, adaptive support, and classroom grounding.
- Do not widen product claims beyond current submission proof.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "app/(utility)/knowledge/page.tsx" "app/(workspace)/dashboard/page.tsx" "app/(workspace)/agents/[botId]/chat/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/contest/CoreLoopVisibilityStrip.tsx"`
- `cd web && npm run build`

## Handoff

- Wording now consistently frames the product as a teacher-controlled adaptive tutor loop across Dashboard, Tutor, Knowledge, and Spec Pack authoring surfaces.
- No runtime behavior, routes, or submission-package docs were changed.
