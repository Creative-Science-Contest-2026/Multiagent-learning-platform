# Hide Guided Learning and Co-Writer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hide Guided Learning and Co-Writer from the visible shell and redirect direct route access back to `/playground` without deleting underlying implementation.

**Architecture:** Remove FE entry points in the sidebar, add route-level redirects at the route wrapper layer so page internals stay intact, and neutralize Knowledge-page session links that still point into Guided Learning. Keep implementation code dormant but present.

**Tech Stack:** Next.js App Router, React, TypeScript, node test, ESLint

---

### Task 1: Remove visible navigation entries

**Files:**
- Modify: `web/components/sidebar/nav-groups.ts`
- Test: `web/tests/sidebar-nav-groups.test.ts`

- [ ] Update the secondary tool list to remove `/guide` and `/co-writer`.
- [ ] Update the sidebar regression test so the expanded secondary-tools group now contains only `/playground` and `/memory`.
- [ ] Run: `cd web && node --test tests/sidebar-nav-groups.test.ts`

### Task 2: Block direct route access without deleting page internals

**Files:**
- Create: `web/app/(workspace)/guide/layout.tsx`
- Create: `web/app/(workspace)/co-writer/layout.tsx`

- [ ] Add a layout-level redirect for `/guide` that immediately sends users to `/playground`.
- [ ] Add the same layout-level redirect for `/co-writer`.
- [ ] Keep the existing `page.tsx` implementations untouched so the underlying code remains in the repo.

### Task 3: Remove routine FE deep links back into Guided Learning

**Files:**
- Modify: `web/app/(utility)/knowledge/page.tsx`

- [ ] Change Knowledge-page notebook record navigation so only `chat` records expose an open-session action.
- [ ] Remove the normal-path button that opens guided-learning sessions from saved records.
- [ ] Keep guided-learning record badges and saved content visible; only the active route entry should disappear.

### Task 4: Validate and record handoff

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-hide-guide-co-writer.md`

- [ ] Run: `cd web && node --test tests/sidebar-nav-groups.test.ts`
- [ ] Run: `cd web && npx eslint "components/sidebar/nav-groups.ts" "app/(workspace)/guide/layout.tsx" "app/(workspace)/co-writer/layout.tsx" "app/(utility)/knowledge/page.tsx"`
- [ ] Run: `cd web && npm run build`
- [ ] Write the PR note with a Mermaid diagram and state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
