# C220 Contest Layout Breakage Sweep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stabilize the contest-path responsive layout, starting with `/agents` spec-pack authoring and then hardening nearby teacher-facing screens against overlap, clipping, and column collapse.

**Architecture:** Keep the fix bounded to presentation. Restack the `/agents` authoring page earlier, add `min-w-0` and wrapping guards to action rows and rails, then apply smaller responsive protections to the cockpit, dashboard, and any confirmed contest-path sibling screen that shares the same failure mode.

**Tech Stack:** Next.js App Router, React, Tailwind utility classes, Node test runner, ESLint

---

### Task 1: Harden `/agents` spec-pack authoring layout

**Files:**
- Modify: `web/components/agents/SpecPackAuthoringTab.tsx`
- Test: existing frontend build and manual verification on `/agents`

- [ ] Restack the root grid so the left rail, authoring column, and summary rail stop competing at laptop widths.
- [ ] Add `min-w-0`, wrapping, and width guards to the top action header and right-rail summary blocks.
- [ ] Make the runtime audit and markdown preview cards tolerate long values without forcing horizontal spill.
- [ ] Run a focused lint/build pass after the `/agents` changes land cleanly.

### Task 2: Apply bounded responsive guards to adjacent contest screens

**Files:**
- Modify: `web/components/contest/TeacherCockpit.tsx`
- Modify: `web/components/contest/CoreLoopVisibilityStrip.tsx`
- Modify: `web/app/(workspace)/dashboard/page.tsx`
- Modify: `web/app/(utility)/knowledge/page.tsx`
- Modify only if needed: `web/app/(utility)/marketplace/page.tsx`

- [ ] Tighten cockpit action-card and header wrapping so longer copy does not crowd controls.
- [ ] Verify the core-loop pill strip wraps cleanly with no clipped labels.
- [ ] Add only the minimum responsive fixes needed on Dashboard and Knowledge if the same overflow pattern appears there.
- [ ] Leave Marketplace untouched unless the code survey confirms the same contest-path issue.

### Task 3: Validate and document lane state

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-30.md`
- Modify: `docs/superpowers/pr-notes/2026-04-30-c220-contest-layout-breakage-sweep.md`

- [ ] Run `cd web && npx eslint "components/agents/SpecPackAuthoringTab.tsx" "app/(workspace)/agents/page.tsx" "components/contest/TeacherCockpit.tsx" "components/contest/CoreLoopVisibilityStrip.tsx" "app/(workspace)/dashboard/page.tsx" "app/(utility)/knowledge/page.tsx" "app/(utility)/marketplace/page.tsx"`.
- [ ] Run `cd web && npm run build`.
- [ ] Run `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null` and `git diff --check`.
- [ ] Update the task registry, daily log, and PR note with the validated impact surface and any residual follow-up for `C221`.
