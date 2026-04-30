# Feature Task: Hide Guided Learning and Co-Writer

Task ID: `UI_HIDE_GUIDE_CO_WRITER`
Commit tag: `UI-HIDE-GUIDE-CO-WRITER`
Owner: Frontend shell reduction lane
Branch: `fix/hide-guide-co-writer`
GitHub Issue:
Active assignment: `ai_first/ACTIVE_ASSIGNMENTS.md`

## Goal

Remove `Học có hướng dẫn` and `Trợ lý soạn thảo` from the visible frontend shell and block direct access to their workspace routes, while keeping the underlying implementation in the repository for future use.

## User-visible outcome

- Sidebar navigation no longer shows Guided Learning or Co-Writer.
- Direct visits to `/guide` and `/co-writer` no longer open those tools and instead send the user back to `/playground`.
- Existing code remains in place and is not deleted.

## Owned files/modules

- `web/components/sidebar/nav-groups.ts`
- `web/app/(workspace)/guide/layout.tsx`
- `web/app/(workspace)/co-writer/layout.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/tests/sidebar-nav-groups.test.ts`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-hide-guide-co-writer.md`
- `docs/superpowers/specs/2026-04-30-hide-guide-co-writer-design.md`
- `docs/superpowers/plans/2026-04-30-hide-guide-co-writer.md`
- `docs/superpowers/pr-notes/2026-04-30-hide-guide-co-writer.md`

## Do-not-touch files/modules

- `deeptutor/**`
- `web/app/(workspace)/agents/**`
- `web/app/(workspace)/dashboard/**`
- `web/app/(utility)/marketplace/**`
- `web/app/(utility)/settings/**`
- `web/app/(workspace)/guide/page.tsx`
- `web/app/(workspace)/guide/hooks/**`
- `web/app/(workspace)/guide/components/**`
- `web/app/(workspace)/co-writer/page.tsx`
- `web/app/(workspace)/co-writer/sampleTemplate.ts`
- `.github/workflows/**`
- `requirements/**`
- `package-lock.json`
- `web/package-lock.json`
- `.env*`

## Design before implementation

### Current behavior

- The sidebar still exposes `/guide` and `/co-writer` as secondary tools.
- Direct navigation to `/guide` and `/co-writer` still opens those experiences.
- The Knowledge screen still contains a branch that deep-links guided-learning records back into `/guide`.

### Intended behavior change

- Remove Guided Learning and Co-Writer from visible sidebar navigation.
- Redirect direct hits to `/guide` and `/co-writer` back to `/playground`.
- Remove or neutralize remaining visible FE deep links that would send normal users back into `/guide`.
- Keep the feature code in place for future reactivation.

### Candidate approaches

1. Hide only the sidebar entries.
   - Smallest diff, but users can still open the tools directly or via remaining deep links.
2. Hide sidebar entries and redirect `/guide` plus `/co-writer` back to `/playground`.
   - Chosen approach because it meets the requirement without deleting underlying implementation.
3. Hide FE and disable all related backend APIs.
   - Too broad for this phase and unnecessary if direct route access is already blocked.

### Chosen approach

Use approach 2. Treat the work as a frontend gating pass: remove navigation entry points, redirect route entry points, and neutralize obvious FE deep links that still assume Guided Learning remains public.

### Codebase survey

- Entry points or handlers:
  - `web/components/sidebar/nav-groups.ts`
  - `web/app/(workspace)/guide/page.tsx`
  - `web/app/(workspace)/co-writer/page.tsx`
- Adjacent or reused flows:
  - `web/app/(utility)/knowledge/page.tsx` currently links guided-learning records back into `/guide`
- Shared contracts, schemas, or types reviewed:
  - guided-learning record types in Knowledge route display logic
- Closest existing tests:
  - `web/tests/sidebar-nav-groups.test.ts`
  - `web/tests/contest-vietnamese-coverage.test.ts`

### Expected impact surface

- Likely to change:
  - sidebar grouping data
  - guide and co-writer route entry behavior
  - knowledge-page deep-link behavior for guided-learning records
  - localized strings only if needed for changed visible labels
  - one focused sidebar test
- Reviewed but expected to remain unchanged:
  - guide internal hooks and components
  - co-writer internals and sample template
  - backend guide APIs and persistence layer unless a narrow comment is needed
- Validation paths:
  - focused sidebar/unit tests
  - targeted lint on touched files
  - production frontend build

## Acceptance criteria

- `Guided Learning` and `Co-Writer` are no longer visible in the sidebar.
- Visiting `/guide` or `/co-writer` redirects to `/playground`.
- No implementation files for those features are deleted.

## Required tests

- `cd web && node --test tests/sidebar-nav-groups.test.ts`
- `cd web && npx eslint "components/sidebar/nav-groups.ts" "app/(workspace)/guide/layout.tsx" "app/(workspace)/co-writer/layout.tsx" "app/(utility)/knowledge/page.tsx"`
- `cd web && npm run build`

## Manual verification

- Confirm sidebar no longer shows Guided Learning or Co-Writer.
- Open `/guide` and `/co-writer` directly and confirm redirect to `/playground`.
- Inspect Knowledge records UI and confirm no normal-path action still opens `/guide`.

## Handoff notes

- Do not delete Guided Learning or Co-Writer internals in this lane.
- Prefer redirect plus UI hiding over backend shutdown.
