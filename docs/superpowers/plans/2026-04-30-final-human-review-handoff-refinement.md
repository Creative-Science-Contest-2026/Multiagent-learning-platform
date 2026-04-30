# Final Human Review Handoff Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** tighten the final human-review docs so the remaining manual contest gates are accurate after the refreshed browser evidence merge

**Architecture:** this is a docs-only cleanup lane. Update the short human-review handoff as the primary operator gate sheet, then align the compact submission checklist so it reflects the same manual completion truth without claiming sign-off has already happened.

**Tech Stack:** Markdown, git diff validation, ripgrep

---

### Task 1: Refresh the human gate sheet

**Files:**
- Modify: `docs/contest/HUMAN_REVIEW_HANDOFF.md`

- [ ] Step 1: replace any stale screenshot-state wording with the current merged evidence state from PR `#243`
- [ ] Step 2: compress the gate list so each remaining manual decision has a clear owner, status, and acceptance rule
- [ ] Step 3: make the suggested read order and expected end state short enough for a final operator pass

### Task 2: Align the compact submission checklist

**Files:**
- Modify: `ai_first/competition/submission-checklist.md`

- [ ] Step 1: keep screenshot evidence checked as complete
- [ ] Step 2: keep `IP commitment reviewed` and `Final package reviewed by humans` unchecked
- [ ] Step 3: tighten the verification basis so it points reviewers at the current handoff and evidence docs

### Task 3: Record and verify the lane

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-final-human-review-handoff-refinement.md`

- [ ] Step 1: record the lane outcome in the daily log
- [ ] Step 2: clear the active assignment after verification
- [ ] Step 3: add the PR note with Mermaid diagram
- [ ] Step 4: run the required `rg` validation and `git diff --check`
