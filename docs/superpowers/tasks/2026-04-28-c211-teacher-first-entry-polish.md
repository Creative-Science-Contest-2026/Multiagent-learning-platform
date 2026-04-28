# 2026-04-28 C211 Teacher-First Entry Polish

- Task ID: `C211_TEACHER_FIRST_ENTRY_POLISH`
- Commit tag: `C211`
- Branch: `fix/submission-close-c211`
- Worktree: `.worktrees/submission-close-c211`
- Status: `in-progress`

## Goal

Improve the first product impression so the contest-facing teacher entry surfaces read immediately as classroom software guided by a teacher, not a generic AI workspace.

## Owned files

- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/contest/CoreLoopVisibilityStrip.tsx`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-28.md`
- `docs/superpowers/tasks/2026-04-28-c211-teacher-first-entry-polish.md`
- `docs/superpowers/pr-notes/2026-04-28-c211-teacher-first-entry-polish.md`

## Do-not-touch

- Runtime or backend logic
- Contest submission package docs
- Validation and evidence docs owned by Session B
- Screenshot assets and evidence inventory order
- Lockfiles and generated files

## Execution notes

- Keep the change bounded to wording and small presentational cues on existing teacher-entry surfaces.
- Preserve existing page structure, routing, and component boundaries.
- Prefer terms like teacher-controlled, classroom setup, and class tutor over generic AI workspace language.
- Do not widen product claims beyond the validated-prototype contract already merged on `main`.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "app/(utility)/knowledge/page.tsx" "app/(workspace)/agents/page.tsx" "app/(workspace)/agents/[botId]/chat/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/contest/CoreLoopVisibilityStrip.tsx"`
- `cd web && npm run build`

## Handoff

- Teacher entry surfaces now read as setup and guided-use flows for a classroom tutor.
- No runtime behavior, routes, submission docs, or evidence assets changed.
