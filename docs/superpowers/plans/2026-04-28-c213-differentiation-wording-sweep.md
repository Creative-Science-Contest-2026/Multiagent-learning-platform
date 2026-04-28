# C213 Differentiation Wording Sweep Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align contest-facing UI copy with the teacher-controlled adaptive tutor framing without changing behavior.

**Architecture:** This plan is a wording-only sweep across existing frontend surfaces plus the required AI-first tracking mirrors. The implementation keeps existing components and flows intact, changing only contest-facing text and control-plane task status.

**Tech Stack:** Next.js, React, TypeScript, Tailwind CSS, Markdown AI-first operating docs

---

### Task 1: Open the `C213` lane contract

**Files:**
- Create: `docs/superpowers/tasks/2026-04-28-c213-differentiation-wording-sweep.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-c213-differentiation-wording-sweep.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-28.md`

- [ ] **Step 1: Write the lane packet and PR note**

```md
Task ID: C213_DIFFERENTIATION_WORDING_SWEEP
Commit tag: C213
Scope: wording-only sweep on bounded contest-facing frontend surfaces
```

- [ ] **Step 2: Move the AI-first mirrors to the active lane**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: command exits successfully after `C212` is recorded as completed and `C213` is recorded as in-progress.

- [ ] **Step 3: Record the daily log handoff**

```md
## C213_DIFFERENTIATION_WORDING_SWEEP
- Branch: `fix/submission-close-c213`
- Task: `C213_DIFFERENTIATION_WORDING_SWEEP`
- Done: opened bounded wording-only polish lane
```

### Task 2: Reframe the contest-facing copy

**Files:**
- Modify: `web/app/(workspace)/dashboard/page.tsx`
- Modify: `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- Modify: `web/app/(utility)/knowledge/page.tsx`
- Modify: `web/components/agents/SpecPackAuthoringTab.tsx`
- Modify: `web/components/contest/CoreLoopVisibilityStrip.tsx`

- [ ] **Step 1: Update the dashboard hero and helper text**

```tsx
{t("Teacher-controlled adaptive loop")}
{t("Teacher-reviewed signals, adaptive next steps")}
{t("Review observed evidence first, then choose the clearest adaptive classroom move for each student or group.")}
```

- [ ] **Step 2: Update tutor chat framing**

```tsx
helperText={t("Tutor replies provide adaptive practice inside the same teacher-controlled loop before diagnosis review and intervention selection.")}
{t("Continue guided tutoring with {{name}}", { name: bot?.name ?? botId })}
```

- [ ] **Step 3: Update knowledge and spec-pack framing**

```tsx
helperText={t("Start with teacher-owned source material so the adaptive tutor, assessment, and teacher review all stay grounded in the same classroom knowledge pack.")}
{t("Shape the adaptive tutor for this class")}
{t("No spec packs yet. Start with a teacher-controlled adaptive tutor.")}
```

- [ ] **Step 4: Keep the shared strip default aligned**

```tsx
{helperText || t("Track the same teacher-guided adaptive loop across the product.")}
```

### Task 3: Validate and prepare review

**Files:**
- Modify: `docs/superpowers/tasks/2026-04-28-c213-differentiation-wording-sweep.md`

- [ ] **Step 1: Run targeted validation**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: PASS

Run: `git diff --check`
Expected: no output

Run: `cd web && npx eslint "app/(utility)/knowledge/page.tsx" "app/(workspace)/dashboard/page.tsx" "app/(workspace)/agents/[botId]/chat/page.tsx" "components/agents/SpecPackAuthoringTab.tsx" "components/contest/CoreLoopVisibilityStrip.tsx"`
Expected: PASS

Run: `cd web && npm run build`
Expected: production build succeeds

- [ ] **Step 2: Update the task packet with validation evidence and merge status**

```md
Validation:
- `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
- `git diff --check`
- `cd web && npx eslint ...`
- `cd web && npm run build`
```

- [ ] **Step 3: Commit**

```bash
git add ai_first/TASK_REGISTRY.json ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-28.md docs/superpowers/tasks/2026-04-28-c213-differentiation-wording-sweep.md docs/superpowers/pr-notes/2026-04-28-c213-differentiation-wording-sweep.md web/app/(workspace)/dashboard/page.tsx web/app/(workspace)/agents/[botId]/chat/page.tsx web/app/(utility)/knowledge/page.tsx web/components/agents/SpecPackAuthoringTab.tsx web/components/contest/CoreLoopVisibilityStrip.tsx
git commit -m "fix(copy): align adaptive tutor framing [C213]"
```
