# Teacher Dashboard Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the teacher dashboard so non-technical Vietnamese teachers can immediately see what needs attention and what action to take next.

**Architecture:** Keep backend payloads unchanged and move the language simplification into a pure presenter helper plus a bounded UI layout refresh. The dashboard page will be reorganized into a clear teaching-priority flow while existing actions and child routes stay intact.

**Tech Stack:** Next.js App Router, React, TypeScript, `react-i18next`, Node test runner, ESLint

---

### Task 1: Lock the teacher-facing wording in tests

**Files:**
- Create: `web/tests/teacher-dashboard-copy.test.ts`
- Modify: `web/tests/contest-terminology.test.ts`
- Modify later: `web/components/dashboard/dashboard-presenters.ts`

- [ ] Add a failing test file for dashboard presenter copy and priority wording.
- [ ] Run `cd web && node --test tests/teacher-dashboard-copy.test.ts` and confirm it fails because the presenter module does not exist yet.
- [ ] Add any bounded locale/terminology assertions needed for the refreshed dashboard wording.

### Task 2: Implement the presenter helper

**Files:**
- Create: `web/components/dashboard/dashboard-presenters.ts`
- Test: `web/tests/teacher-dashboard-copy.test.ts`

- [ ] Implement pure mapping helpers for confidence labels, support-level labels, activity labels, activity-status labels, and top-summary content.
- [ ] Re-run `cd web && node --test tests/teacher-dashboard-copy.test.ts` and confirm it passes.

### Task 3: Refresh the dashboard layout and copy

**Files:**
- Modify: `web/app/(workspace)/dashboard/page.tsx`
- Modify: `web/components/dashboard/TeacherInsightPanel.tsx`
- Modify: `web/components/dashboard/StudentInsightCard.tsx`
- Modify: `web/components/dashboard/SmallGroupInsightCard.tsx`
- Modify: `web/locales/en/app.json`
- Modify: `web/locales/vi/app.json`

- [ ] Rework the dashboard page so the teacher-priority summary and insight section come first, with supporting metrics/history below.
- [ ] Update the teacher insight section heading and helper copy to Vietnamese-first classroom wording.
- [ ] Redesign the student insight card so evidence, interpretation, and suggested action read as one connected story.
- [ ] Route technical backend values through the presenter helper instead of exposing raw snake_case terms.

### Task 4: Validate and record the lane

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-teacher-dashboard-refresh.md`

- [ ] Run `cd web && node --test tests/contest-terminology.test.ts tests/teacher-dashboard-copy.test.ts`.
- [ ] Run `cd web && npx eslint "app/(workspace)/dashboard/page.tsx" "components/dashboard/TeacherInsightPanel.tsx" "components/dashboard/StudentInsightCard.tsx" "components/dashboard/dashboard-presenters.ts"`.
- [ ] Run `cd web && npm run build`.
- [ ] Run `git diff --check`.
- [ ] Record the work in the daily log and write the required PR note with a Mermaid diagram.
