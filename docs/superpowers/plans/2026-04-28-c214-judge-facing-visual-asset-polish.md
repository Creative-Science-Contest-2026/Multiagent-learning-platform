# C214 Judge-Facing Visual Asset Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve judge-facing screenshot captions and presentation order without changing evidence artifacts or product scope.

**Architecture:** This is a docs-only evidence packaging pass. The plan updates the evidence entry points and AI-first mirrors so the same screenshot set reads more clearly as teacher control plus adaptive loop proof.

**Tech Stack:** Markdown docs, AI-first operating files

---

### Task 1: Open the `C214` docs lane

**Files:**
- Create: `docs/superpowers/tasks/2026-04-28-c214-judge-facing-visual-asset-polish.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-c214-judge-facing-visual-asset-polish.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-28.md`

- [ ] **Step 1: Record `C213` as completed and `C214` as active**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: PASS after the task-state transition.

- [ ] **Step 2: Write the lane packet and PR note**

```md
Task ID: C214_JUDGE_FACING_VISUAL_ASSET_POLISH
Commit tag: C214
Scope: docs and evidence inventory only
```

### Task 2: Improve judge-facing screenshot guidance

**Files:**
- Modify: `docs/contest/README.md`
- Modify: `docs/contest/EVIDENCE_CHECKLIST.md`
- Modify: `docs/contest/SUBMISSION_PACKAGE.md`
- Modify: `ai_first/evidence/screenshots.md`

- [ ] **Step 1: Add recommended judge-view order**

```md
1. Teacher control
2. Knowledge grounding
3. Assessment evidence
4. Tutor support
5. Dashboard review
```

- [ ] **Step 2: Add caption intent to the screenshot inventory**

```md
Judge-facing caption: "Teacher sets the learning context and sharing boundary before any AI step begins."
```

- [ ] **Step 3: Keep claims bounded**

```md
Use the screenshot set to support the validated prototype story only; do not imply classroom outcome proof or autonomous teacher replacement.
```

### Task 3: Validate and prepare merge

**Files:**
- Modify: `docs/superpowers/tasks/2026-04-28-c214-judge-facing-visual-asset-polish.md`

- [ ] **Step 1: Run docs validation**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: PASS

Run: `rg -n "judge-facing|caption|visual order|teacher control|adaptive loop" docs/contest ai_first/evidence docs/superpowers/tasks docs/superpowers/pr-notes`
Expected: matches the new caption/order guidance

Run: `git diff --check`
Expected: no output

- [ ] **Step 2: Commit**

```bash
git add ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-28.md docs/contest/README.md docs/contest/EVIDENCE_CHECKLIST.md docs/contest/SUBMISSION_PACKAGE.md ai_first/evidence/screenshots.md docs/superpowers/tasks/2026-04-28-c214-judge-facing-visual-asset-polish.md docs/superpowers/pr-notes/2026-04-28-c214-judge-facing-visual-asset-polish.md
git commit -m "docs(evidence): polish judge-facing asset guidance [C214]"
```
