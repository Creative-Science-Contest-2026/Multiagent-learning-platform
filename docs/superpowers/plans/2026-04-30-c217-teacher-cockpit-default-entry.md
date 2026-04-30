# C217 Teacher Cockpit Default Entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `/` into a teacher-first cockpit and preserve the broader workspace as a secondary route.

**Architecture:** Introduce a small contest cockpit component and one content helper, then update the shell's secondary chat path to point at `/playground`. Keep all actions link-based and avoid backend or localization expansion in this slice.

**Tech Stack:** Next.js App Router, React, TypeScript, existing node:test frontend utility tests, ESLint

---

### Task 1: Add failing tests for cockpit content and secondary chat path

**Files:**
- Create: `web/tests/teacher-cockpit-content.test.ts`
- Modify: `web/tests/sidebar-nav-groups.test.ts`

- [ ] **Step 1: Write the failing tests**

Add tests asserting:
- the cockpit primary actions point to `/knowledge`, `/agents`, `/dashboard`, and `/marketplace`
- the cockpit support action for the broader workspace points to `/playground`
- the sidebar secondary chat/tool route uses `/playground`

- [ ] **Step 2: Run test to verify it fails**

Run:
- `node --test web/tests/teacher-cockpit-content.test.ts web/tests/sidebar-nav-groups.test.ts`

Expected: FAIL because the cockpit content helper does not exist yet and the sidebar still treats `/` as the chat path.

- [ ] **Step 3: Write minimal implementation**

Add the content helper and update sidebar nav grouping so tests can pass.

- [ ] **Step 4: Run test to verify it passes**

Run:
- `node --test web/tests/teacher-cockpit-content.test.ts web/tests/sidebar-nav-groups.test.ts`

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web/tests/teacher-cockpit-content.test.ts web/tests/sidebar-nav-groups.test.ts web/components/contest/teacher-cockpit-content.ts web/components/sidebar/nav-groups.ts
git commit -m "test(contest): cover teacher cockpit entry [C217]"
```

### Task 2: Replace `/` with the teacher cockpit

**Files:**
- Create: `web/components/contest/TeacherCockpit.tsx`
- Modify: `web/app/(workspace)/page.tsx`
- Modify: `web/components/sidebar/SidebarShell.tsx`

- [ ] **Step 1: Implement the bounded cockpit**

Render a teacher-first hero, the core loop strip, primary action cards, and one secondary path into `/playground`.

- [ ] **Step 2: Keep broad workspace as a secondary route**

Update the shell path or supporting link so users can still reach the broader tool surface intentionally.

- [ ] **Step 3: Run packet validation**

Run:
- `cd web && npx eslint "app/(workspace)/page.tsx" "app/(workspace)/dashboard/page.tsx" "components/sidebar/SidebarShell.tsx" components/contest/*.tsx`
- `cd web && npm run build`
- `git diff --check`

Expected: all commands pass

- [ ] **Step 4: Commit**

```bash
git add web/app/'(workspace)'/page.tsx web/components/contest/TeacherCockpit.tsx web/components/sidebar/SidebarShell.tsx
git commit -m "feat(contest): add teacher cockpit default entry [C217]"
```
