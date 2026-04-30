# Code Review Graph Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install `code-review-graph`, configure this repository for Codex, and commit the initial repo-local graph artifacts if the tool creates them.

**Architecture:** Keep the Python package installation machine-level so the repo does not gain a tracked dependency, then run the upstream Codex integration inside the dedicated worktree so only repo-local instructions and generated graph assets change. Validate with the upstream CLI plus diff checks before staging the bounded artifact set.

**Tech Stack:** Python 3.12, `code-review-graph` CLI, Codex repo instructions, MCP config, git worktree

---

### Task 1: Install The CLI On This Machine

**Files:**
- Modify: no tracked repo files
- Test: command availability only

- [ ] **Step 1: Install `code-review-graph` with an isolated machine-level tool path**

```bash
python3 -m pip install --user code-review-graph
```

- [ ] **Step 2: Verify the executable is available**

Run: `~/Library/Python/3.12/bin/code-review-graph --help`
Expected: command help prints with `install`, `build`, and `status` subcommands.

### Task 2: Configure This Repository For Codex

**Files:**
- Modify: `.gitignore`
- Create: `.claude/skills/*.md`

- [ ] **Step 1: Run the upstream Codex installation flow inside the dedicated worktree**

```bash
~/Library/Python/3.12/bin/code-review-graph install --platform codex
```

- [ ] **Step 2: Inspect which repo-local files changed**

Run: `git status --short`
Expected: only the bounded tooling files are added or modified, primarily `.gitignore` and `.claude/skills/*.md`.

### Task 3: Build And Inspect The Initial Graph Artifact

**Files:**
- Create or modify: `.code-review-graph/`

- [ ] **Step 1: Build the graph for this repository**

```bash
~/Library/Python/3.12/bin/code-review-graph build
```

- [ ] **Step 2: Check graph health and output location**

Run: `~/Library/Python/3.12/bin/code-review-graph status`
Expected: the command reports graph metadata for the current repository and confirms the build completed.

- [ ] **Step 3: Inspect the generated artifact set**

Run: `find .code-review-graph -maxdepth 2 -type f | sort`
Expected: repo-local graph files are listed if the tool stores them under `.code-review-graph/`.

### Task 4: Review, Record, And Commit The Bounded Integration

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-code-review-graph-integration.md`
- Review: `.gitignore`, `.claude/skills/`, `.code-review-graph/`

- [ ] **Step 1: Record the integration result in the daily log and PR note**

```text
Capture the exact files created by install/build, whether `.code-review-graph/` was generated, and the verification commands that passed.
```

- [ ] **Step 2: Check for malformed whitespace before staging**

Run: `git diff --check`
Expected: no whitespace or patch-format errors.

- [ ] **Step 3: Stage only the bounded integration files**

```bash
git add .gitignore .claude/skills .code-review-graph ai_first/ACTIVE_ASSIGNMENTS.md ai_first/daily/2026-04-30.md docs/superpowers/tasks/2026-04-30-code-review-graph-integration.md docs/superpowers/specs/2026-04-30-code-review-graph-integration-design.md docs/superpowers/plans/2026-04-30-code-review-graph-integration.md docs/superpowers/pr-notes/2026-04-30-code-review-graph-integration.md
```

- [ ] **Step 4: Commit with the lane task identifier**

```bash
git commit -m "chore(tooling): integrate code-review-graph for Codex [OPS_CODE_REVIEW_GRAPH_INTEGRATION]"
```
