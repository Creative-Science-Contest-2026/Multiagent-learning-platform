# C216 Contest Shell Scope Trim Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the shared sidebar shell so contest-core routes are visually primary and inherited DeepTutor tools are clearly secondary.

**Architecture:** Keep the existing shared `SidebarShell` as the only place that owns route grouping. Add a small test harness around the shell, then implement grouped rendering without changing route targets, session logic, or locale contracts.

**Tech Stack:** Next.js App Router, React, TypeScript, existing frontend test runner, ESLint

---

### Task 1: Add focused shell tests

**Files:**
- Create: `web/components/sidebar/__tests__/SidebarShell.test.tsx`
- Modify: `web/components/sidebar/SidebarShell.tsx`

- [ ] **Step 1: Write the failing tests**

Write tests that assert:
- expanded mode shows a contest-core section before a secondary-tools section
- expanded mode still renders `Knowledge`, `Dashboard`, `/agents`, and `Marketplace`
- collapsed mode omits secondary tool links such as `Co-Writer` and `Memory`

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web && npm test -- SidebarShell.test.tsx`
Expected: FAIL because the current shell has one flat nav and no grouped structure.

- [ ] **Step 3: Write minimal implementation**

Implement grouped nav metadata and render logic in `SidebarShell.tsx`, reusing existing route targets and active-state behavior.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web && npm test -- SidebarShell.test.tsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web/components/sidebar/SidebarShell.tsx web/components/sidebar/__tests__/SidebarShell.test.tsx
git commit -m "test(sidebar): cover contest shell grouping [C216]"
```

### Task 2: Validate shell integration

**Files:**
- Modify: `web/components/sidebar/WorkspaceSidebar.tsx`
- Modify: `web/components/sidebar/UtilitySidebar.tsx`
- Modify: `web/app/(workspace)/layout.tsx`
- Modify: `web/app/(utility)/layout.tsx`

- [ ] **Step 1: Inspect whether companion wrappers need changes**

Confirm the grouped shell works with current wrappers. Only adjust wrapper props or layout spacing if the grouped shell exposes a visual bug or dead path.

- [ ] **Step 2: Implement the smallest companion adjustments**

Keep wrapper behavior the same unless one tiny shell-alignment fix is required.

- [ ] **Step 3: Run the packet validation commands**

Run:
- `cd web && npx eslint "components/sidebar/SidebarShell.tsx" "components/sidebar/WorkspaceSidebar.tsx" "components/sidebar/UtilitySidebar.tsx" "app/(workspace)/layout.tsx" "app/(utility)/layout.tsx"`
- `cd web && npm run build`
- `git diff --check`

Expected: all commands pass

- [ ] **Step 4: Commit**

```bash
git add web/components/sidebar/WorkspaceSidebar.tsx web/components/sidebar/UtilitySidebar.tsx web/app/'(workspace)'/layout.tsx web/app/'(utility)'/layout.tsx
git commit -m "feat(sidebar): trim contest shell scope [C216]"
```
