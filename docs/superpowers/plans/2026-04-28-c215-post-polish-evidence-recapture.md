# C215 Post-Polish Evidence Recapture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update contest evidence docs so they correctly separate current command-backed proof from stale browser screenshots after the latest Phase 2 polish merges.

**Architecture:** This is a docs-only truth-alignment pass. It does not create new evidence; it adjusts freshness labels, caveats, and operator guidance so the evidence bundle reflects the current merged UI state.

**Tech Stack:** Markdown docs, AI-first operating files

---

### Task 1: Open the `C215` evidence lane

**Files:**
- Create: `docs/superpowers/tasks/2026-04-28-c215-post-polish-evidence-recapture.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-c215-post-polish-evidence-recapture.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-28.md`

- [ ] **Step 1: Record `C214` as completed and `C215` as active**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: PASS

- [ ] **Step 2: Write the lane packet and PR note**

```md
Task ID: C215_POST_POLISH_EVIDENCE_RECAPTURE
Commit tag: C215
Scope: evidence freshness docs only
```

### Task 2: Correct browser-evidence freshness states

**Files:**
- Modify: `docs/contest/VALIDATION_REPORT.md`
- Modify: `docs/contest/EVIDENCE_CHECKLIST.md`
- Modify: `docs/contest/SUBMISSION_PACKAGE.md`
- Modify: `ai_first/evidence/screenshots.md`

- [ ] **Step 1: Mark changed screenshot groups as stale**

```md
Browser screenshots remain on 2026-04-25 or 2026-04-26 captures and are now stale after Phase 2 polish merges `#214`, `#215`, and `#216`.
```

- [ ] **Step 2: Keep command-backed evidence current**

```md
The 2026-04-28 smoke-backed command evidence remains current because no later smoke run has replaced it.
```

- [ ] **Step 3: Add the next required recapture step**

```md
Next required action: perform one browser recapture pass after the current merged UI is running locally, then restore screenshot rows to `Current`.
```

### Task 3: Validate and prepare merge

**Files:**
- Modify: `docs/superpowers/tasks/2026-04-28-c215-post-polish-evidence-recapture.md`

- [ ] **Step 1: Run docs validation**

Run: `python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
Expected: PASS

Run: `rg -n "Stale|Current|post-polish|browser screenshots|recapture|#214|#215|#216" docs/contest ai_first/evidence docs/superpowers/tasks docs/superpowers/pr-notes`
Expected: matches the updated freshness and recapture guidance

Run: `git diff --check`
Expected: no output

- [ ] **Step 2: Commit**

```bash
git add ai_first/ACTIVE_ASSIGNMENTS.md ai_first/TASK_REGISTRY.json ai_first/daily/2026-04-28.md ai_first/evidence/screenshots.md docs/contest/VALIDATION_REPORT.md docs/contest/EVIDENCE_CHECKLIST.md docs/contest/SUBMISSION_PACKAGE.md docs/superpowers/tasks/2026-04-28-c215-post-polish-evidence-recapture.md docs/superpowers/pr-notes/2026-04-28-c215-post-polish-evidence-recapture.md
git commit -m "docs(evidence): sync post-polish freshness states [C215]"
```
