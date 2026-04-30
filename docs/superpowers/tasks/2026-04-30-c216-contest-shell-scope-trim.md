# 2026-04-30 C216 Contest Shell Scope Trim

- Task ID: `C216_CONTEST_SHELL_SCOPE_TRIM`
- Commit tag: `C216`
- Branch: `fix/contest-shell-scope-trim`
- Worktree: `.worktrees/contest-shell-scope-trim`
- Status: `pending`

## Goal

Demote inherited DeepTutor workspace routes from the primary contest shell so judges and presenters see one bounded classroom product path instead of a broad multi-tool workspace.

## User-visible outcome

- Primary sidebar navigation focuses on the contest loop and teacher setup path.
- Non-core inherited surfaces no longer compete visually with Knowledge, Assessment, Tutor, Dashboard, and `/agents` during the main demo.
- The shell still allows internal access to existing routes when needed, but the contest-first information architecture is obvious on first load.

## Owned files

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx`
- `web/components/sidebar/UtilitySidebar.tsx`
- `web/app/(workspace)/layout.tsx`
- `web/app/(utility)/layout.tsx`
- `ai_first/TASK_REGISTRY.json`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-c216-contest-shell-scope-trim.md`
- `docs/superpowers/pr-notes/2026-04-30-c216-contest-shell-scope-trim.md`

## Do-not-touch

- `web/app/(workspace)/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/app/(utility)/marketplace/page.tsx`
- `web/locales/`
- `deeptutor/`
- contest submission docs under `docs/contest/`
- lockfiles and generated files

## Execution notes

- Keep the change shell-only. Do not change runtime behavior, route implementations, or API contracts.
- Do not rename the product or introduce a new default landing route here. Brand and copy cleanup belongs to `C218`; default entry changes belong to `C217`.
- Prefer contest-first prioritization over deletion:
  - promote `Knowledge`, `Dashboard`, and `/agents`;
  - demote or visually isolate inherited routes such as `Chat`, `Co-Writer`, `Guided Learning`, and `Memory`;
  - keep access to those routes only if it can remain clearly secondary.
- Preserve mobile and collapsed-sidebar usability.
- If the cleanest solution requires new copy strings in `web/locales/`, stop and split that need into `C218` instead of widening this task.

## Acceptance criteria

- The expanded sidebar no longer presents the inherited broad workspace surface as the primary product story.
- Contest-core routes are grouped and visually prioritized ahead of inherited tools.
- Any retained inherited routes are clearly secondary and do not dominate the first screen.
- No route code, dashboard logic, or tutor logic changes are required.

## Validation

- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint "components/sidebar/SidebarShell.tsx" "components/sidebar/WorkspaceSidebar.tsx" "components/sidebar/UtilitySidebar.tsx" "app/(workspace)/layout.tsx" "app/(utility)/layout.tsx"`
- `cd web && npm run build`

## Manual verification

- Open the workspace shell and confirm the first visual read emphasizes the contest loop surfaces instead of a generic AI workspace.
- Collapse and expand the sidebar to confirm the same prioritization still reads clearly.
- Open at least one non-core inherited route and confirm it remains reachable without reclaiming primary visual priority.

## Parallel-work notes

- This packet is intentionally narrower than `C217`; do not change `/` landing behavior here.
- This packet is intentionally narrower than `C218`; do not widen into product renaming or localization rewrites here.
- If shell trimming reveals that a route should be hidden only in contest mode, record the smallest safe mechanism in the PR note instead of inventing a larger feature flag system.

## PR architecture note

- Must include Mermaid diagram.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` is not expected to change unless the shell routing structure materially changes.

## Handoff

- Next expected follow-up is `C217_TEACHER_COCKPIT_DEFAULT_ENTRY`, which can assume a cleaner contest-first shell already exists.
