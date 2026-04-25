# Two-Lane Contest MVP Polish Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Roll the approved two-lane contest MVP polish design into the AI-first control plane by adding the new backlog, creating task packets, and refreshing coordination state for parallel execution.

**Architecture:** This is a docs-and-control-plane rollout, not product implementation. The work is split into three bounded units: backlog metadata in `ai_first/TASK_REGISTRY.json`, operating-state mirrors in `ai_first/`, and execution contracts in `docs/superpowers/tasks/` plus one PR note. The rollout should leave the repo ready for two accounts to start work without sharing ownership by default.

**Tech Stack:** Markdown, JSON, ripgrep, git, existing AI-first task packet conventions.

---

### Task 1: Add the rollout plan and verify current control-plane context

**Files:**
- Create: `docs/superpowers/plans/2026-04-25-two-lane-contest-mvp-polish-rollout.md`
- Read: `docs/superpowers/specs/2026-04-25-two-lane-contest-mvp-polish-design.md`
- Read: `ai_first/TASK_REGISTRY.json`
- Read: `ai_first/AI_OPERATING_PROMPT.md`
- Read: `ai_first/EXECUTION_QUEUE.md`

- [ ] **Step 1: Confirm branch and working tree**

Run: `git status --short --branch`
Expected: current branch is `docs/t044-two-lane-parallel-backlog` and only the approved spec commit exists.

- [ ] **Step 2: Re-read the approved design and current control plane**

Run:

```bash
sed -n '1,260p' docs/superpowers/specs/2026-04-25-two-lane-contest-mvp-polish-design.md
sed -n '1,220p' ai_first/AI_OPERATING_PROMPT.md
sed -n '1,220p' ai_first/EXECUTION_QUEUE.md
```

Expected: the design names `T044` through `T051`, and the current queue still reflects the older "wait for human review" state.

- [ ] **Step 3: Save this rollout plan**

Content to preserve in this file:

```markdown
# Two-Lane Contest MVP Polish Rollout Implementation Plan
...
```

Expected: the plan exists at `docs/superpowers/plans/2026-04-25-two-lane-contest-mvp-polish-rollout.md`.

- [ ] **Step 4: Commit the plan if it was created separately**

```bash
git add docs/superpowers/plans/2026-04-25-two-lane-contest-mvp-polish-rollout.md
git commit -m "docs: add rollout plan for two-lane contest backlog"
```

Expected: either a new commit exists or the plan is intentionally batched with the rollout commit.

### Task 2: Update backlog metadata and AI-first operating mirrors

**Files:**
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/AI_OPERATING_PROMPT.md`
- Modify: `ai_first/EXECUTION_QUEUE.md`
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/CURRENT_STATE.md`
- Modify: `ai_first/NEXT_ACTIONS.md`
- Modify: `ai_first/daily/2026-04-25.md`

- [ ] **Step 1: Add new tasks `T044` through `T051` to the registry**

Required structure:

```json
{
  "id": "T047_CONTEST_FLOW_OPERATING_HYGIENE_REFRESH",
  "category": "High",
  "priority": 37,
  "title": "Contest Flow Operating Hygiene Refresh",
  "status": "in-progress"
}
```

Rules:
- `total_tasks` becomes `43`
- `completed.count` stays `35`
- `in_progress.count` becomes `2` for `T047` and `T048`
- `pending.count` becomes `6` for `T044`, `T045`, `T046`, `T049`, `T050`, `T051`
- `last_updated` moves to the current rollout time

- [ ] **Step 2: Update the AI operating prompt**

Add the new working state:

```markdown
- Latest operating status: the repo is preparing a two-lane contest MVP polish experiment...
```

And update next actions so the queue no longer says "no further AI lane is required." It should instead point to `T047` bootstrap, then the two-lane experiment.

- [ ] **Step 3: Refresh the execution queue and snapshots**

Required changes:
- `ai_first/EXECUTION_QUEUE.md` should name the two-lane experiment as the active queue
- `ai_first/CURRENT_STATE.md` should stop pointing at the stale `docs/task-registry-count-sync` branch
- `ai_first/NEXT_ACTIONS.md` should list `T047`, `T048`, and then the lane start order

- [ ] **Step 4: Replace the stale assignment board entry**

Update `ai_first/ACTIVE_ASSIGNMENTS.md` so it contains one current assignment:

```markdown
- Owner: Codex
- Task: T047/T048 two-lane contest MVP backlog rollout
- Branch: docs/t044-two-lane-parallel-backlog
```

Expected: no stale `#119` assignment remains.

- [ ] **Step 5: Validate the registry and mirrors**

Run:

```bash
python3 -m json.tool ai_first/TASK_REGISTRY.json >/dev/null
rg -n "T044|T045|T046|T047|T048|T049|T050|T051|two-lane|docs/t044-two-lane-parallel-backlog" ai_first docs/superpowers/specs -S
```

Expected: JSON is valid and the new tasks appear in the control-plane files.

### Task 3: Create task packets and PR note for the rollout

**Files:**
- Create: `docs/superpowers/tasks/2026-04-25-T044-contest-vietnamese-coverage.md`
- Create: `docs/superpowers/tasks/2026-04-25-T045-marketplace-knowledge-polish.md`
- Create: `docs/superpowers/tasks/2026-04-25-T046-dashboard-review-polish.md`
- Create: `docs/superpowers/tasks/2026-04-25-T047-contest-operating-hygiene-refresh.md`
- Create: `docs/superpowers/tasks/2026-04-25-T048-parallel-lane-task-packets.md`
- Create: `docs/superpowers/tasks/2026-04-25-T049-metadata-depth-pass.md`
- Create: `docs/superpowers/tasks/2026-04-25-T050-dashboard-insight-depth.md`
- Create: `docs/superpowers/tasks/2026-04-25-T051-session-context-quality-pass.md`
- Create: `docs/superpowers/pr-notes/2026-04-25-t047-t048-two-lane-rollout.md`

- [ ] **Step 1: Draft task packets using the current template**

Every packet must include:
- owner
- branch
- active assignment pointer
- owned files
- do-not-touch files
- acceptance criteria
- required tests
- parallel-work notes

The packets must reflect the lane boundaries from the approved design.

- [ ] **Step 2: Write the rollout PR note**

It must include:

```markdown
# T047/T048 Two-Lane Contest MVP Rollout
``` 

And one Mermaid diagram describing:
- bootstrap docs refresh
- task packet creation
- handoff into Lane 1 and Lane 2

- [ ] **Step 3: Record the rollout in the daily log**

Add a new 2026-04-25 section covering:
- design approval
- registry expansion to `T044-T051`
- assignment board cleanup
- task packet creation for both lanes

- [ ] **Step 4: Run final validation**

Run:

```bash
git diff --check
rg -n "T044|T045|T046|T047|T048|T049|T050|T051" docs/superpowers/tasks docs/superpowers/pr-notes ai_first -S
```

Expected: no diff formatting errors and all task files are discoverable.

- [ ] **Step 5: Commit the rollout**

```bash
git add ai_first/TASK_REGISTRY.json ai_first/AI_OPERATING_PROMPT.md ai_first/EXECUTION_QUEUE.md ai_first/ACTIVE_ASSIGNMENTS.md ai_first/CURRENT_STATE.md ai_first/NEXT_ACTIONS.md ai_first/daily/2026-04-25.md docs/superpowers/tasks docs/superpowers/pr-notes docs/superpowers/plans/2026-04-25-two-lane-contest-mvp-polish-rollout.md
git commit -m "docs: roll out two-lane contest MVP backlog"
```

Expected: one clean rollout commit is ready for push and PR creation.

## Self-Review

- Spec coverage: Task 2 covers control-plane rollout and registry expansion. Task 3 covers packet creation and PR-note requirements from the design.
- Placeholder scan: no `TODO`, `TBD`, or hand-wavy "appropriate handling" language remains.
- Type consistency: task ids, branch names, and file paths match the approved design and current repo conventions.
