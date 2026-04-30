# Spec: Hide Guided Learning and Co-Writer

Date: 2026-04-30
Task ID: `UI_HIDE_GUIDE_CO_WRITER`
Branch: `fix/hide-guide-co-writer`

## Goal

Temporarily remove `Học có hướng dẫn` and `Trợ lý soạn thảo` from the public web shell without deleting their implementation, so the contest-facing product surface stays narrower and easier to control.

## Current behavior

- The workspace sidebar still shows `Guided Learning` and `Co-Writer`.
- Users can still open `/guide` and `/co-writer` directly.
- The Knowledge page still contains guided-learning session links that reopen `/guide`.

## Intended behavior

- `Guided Learning` and `Co-Writer` should disappear from frontend navigation.
- Direct route access to `/guide` and `/co-writer` should redirect to `/playground`.
- Existing code should remain in the repository for future reactivation.
- The main user shell should no longer offer a visible or routine path back into those tools.

## Approaches considered

### Approach 1: Hide navigation only

Remove the sidebar entries but leave the routes and existing deep links untouched.

- Pros: smallest code diff
- Cons: does not actually block users from opening the tools, so it fails the stated requirement

### Approach 2: Hide navigation and redirect route entry points

Remove visible nav entries and make `/guide` and `/co-writer` redirect to `/playground`. Also neutralize the main FE deep link from Knowledge records that assumes guided learning remains public.

- Pros: satisfies the product requirement while keeping internal code intact
- Pros: low-risk because route-level redirects are easy to reverse later
- Cons: leaves dormant implementation code in place, which is intentional for now

### Approach 3: Hide FE and disable backend APIs

In addition to navigation and route blocking, also disable or comment backend guide/co-writer entry APIs.

- Pros: strongest lockout
- Cons: broader impact surface, more regression risk, unnecessary for the current scope

## Chosen approach

Use approach 2.

This preserves the implementation for future development, minimizes behavior changes outside the user shell, and gives a clean contest-facing surface without broad backend churn.

## Planned changes

### 1. Sidebar navigation

Update the secondary tools list so it no longer includes:

- `/guide`
- `/co-writer`

`/playground` and `/memory` remain visible.

### 2. Route access control

Change the workspace route entry points for:

- `web/app/(workspace)/guide/page.tsx`
- `web/app/(workspace)/co-writer/page.tsx`

Both routes should immediately redirect to `/playground`.

The redirect should happen at the page-entry layer so the route is blocked even if a user types the URL directly.

### 3. Remaining frontend deep links

Review the Knowledge page behavior that currently maps guided-learning records to `/guide`.

If that action is still visible to end users, replace it with a safer fallback:

- either suppress the open action for guided-learning records
- or reroute it to `/playground`

The chosen fallback should avoid exposing `/guide` as an active experience.

## Files expected to change

- `web/components/sidebar/nav-groups.ts`
- `web/app/(workspace)/guide/page.tsx`
- `web/app/(workspace)/co-writer/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `docs/superpowers/tasks/2026-04-30-hide-guide-co-writer.md`
- `docs/superpowers/specs/2026-04-30-hide-guide-co-writer-design.md`
- `ai_first/ACTIVE_ASSIGNMENTS.md`

## Files reviewed but expected to remain unchanged

- `web/app/(workspace)/guide/hooks/**`
- `web/app/(workspace)/guide/components/**`
- `web/app/(workspace)/co-writer/sampleTemplate.ts`
- backend guide APIs and persistence modules

## Testing

- `cd web && node --test tests/sidebar-nav-groups.test.ts`
- `cd web && npx eslint "components/sidebar/nav-groups.ts" "app/(workspace)/guide/page.tsx" "app/(workspace)/co-writer/page.tsx" "app/(utility)/knowledge/page.tsx"`
- `cd web && npm run build`

## Risks

- Knowledge history surfaces may still reference guided-learning records as a type even after the public route is hidden.
- Redirecting route entry points without removing all FE deep links can produce a slightly confusing bounce if a hidden link path remains.

## Out of scope

- Deleting Guided Learning or Co-Writer implementation
- Refactoring backend guide APIs
- Removing saved historical data associated with those tools
