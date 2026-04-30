# C217 Teacher Cockpit Default Entry Design

## Goal

Replace the generic tool-first `/` landing with a teacher-first cockpit that directs the contest demo toward teacher setup, assessment context, tutoring setup, and dashboard follow-up.

## Current behavior

- `web/app/(workspace)/page.tsx` renders the full multi-capability chat workspace directly at `/`.
- The page includes capability pickers, tool toggles, notebook/history hooks, and broad attachment flows, which makes the first read feel like a generic AI workspace.
- After `C216`, the shell already demotes inherited tools, but the main content area at `/` still tells the old story.

## Intended behavior

- `/` should become a bounded cockpit with:
  - one short teacher-first hero;
  - visible contest loop framing;
  - primary actions for Knowledge Pack, class tutor setup, dashboard review, and marketplace/assessment preparation;
  - one explicit secondary route into the broader workspace/tool surface.
- The broader tool surface should remain available as a secondary path, not the default landing.

## Candidate approaches

### Approach 1: Redirect `/` to `/dashboard`

- Pros: tiny patch, almost no new UI.
- Cons: first impression remains tied to one existing screen and does not explain the teacher setup path well.

### Approach 2: Replace `/` with a small cockpit and move broad chat to a secondary route

- Pros: strongest contest-first story, no new APIs, allows one intentional secondary route into the broader workspace.
- Cons: requires a moderate frontend patch and one shell-link adjustment.

## Chosen approach

Use **Approach 2**.

- Implement a new teacher cockpit at `/`.
- Reuse `CoreLoopVisibilityStrip`.
- Keep actions static and link-based.
- Point the secondary general-workspace path to `/playground`, which already exists as a broader capability surface and is close enough to the old exploratory workspace role for this bounded slice.

## Files expected to change

- `web/app/(workspace)/page.tsx`
- `web/components/contest/TeacherCockpit.tsx`
- `web/components/contest/teacher-cockpit-content.ts`
- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/nav-groups.ts`
- `web/tests/teacher-cockpit-content.test.ts`
- `web/tests/sidebar-nav-groups.test.ts`

## Files reviewed but expected unchanged

- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- backend and API client modules

## Tests to add or update

- Add a focused test for cockpit action/support links.
- Update sidebar grouping tests so the secondary `Chat` path resolves to `/playground` instead of `/`.
- Run packet validation lint/build after implementation.
