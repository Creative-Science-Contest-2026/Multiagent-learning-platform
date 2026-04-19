# Demo Readiness Smoke Lane Design

## Context

The contest MVP path is already merged into `main`:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

The repository now also has:

- contest evidence docs and screenshots;
- backend/frontend/docs CI;
- an AI-first control plane with `AI_OPERATING_PROMPT.md`;
- a compact status board in `ai_first/EXECUTION_QUEUE.md`.

What is still missing is a small, repeatable lane that tells an AI worker whether the end-to-end demo path is still alive after important merges. Right now the repo has pieces of evidence and local validation notes, but it does not have one explicit smoke lane that says what to run, how to classify pass/fail, and what becomes the next task if the demo path breaks.

## Goal

Add a `demo readiness / end-to-end smoke validation` lane as the next AI-first operating step, so an AI worker can quickly verify the contest MVP path, record the result, and turn failures into the next task instead of silently drifting.

## Non-Goals

This lane does not:

- replace backend/frontend CI with full browser automation immediately;
- introduce deployment or staging infrastructure;
- add new product features;
- require real production credentials or public hosting;
- attempt full GitHub Actions smoke automation in the first pass.

## User-Facing Outcome

A human or AI worker can open one task packet and one smoke runbook, run a short end-to-end validation flow locally, and know:

- what commands to run;
- what evidence to capture or refresh;
- what counts as pass/fail;
- what the next task is if any stage fails.

## Constraints

- Keep round 1 docs/workflow-first.
- Avoid touching `package-lock.json`, `web/next-env.d.ts`, runtime code, or dependency files unless the smoke lane proves a narrow fix is necessary in a follow-up task.
- Reuse the existing contest evidence docs and AI-first control plane instead of creating a second system.
- Keep the smoke lane small enough that AI can run it after major merges without spending the whole night on orchestration.

## Approaches

### Approach 1: Docs-first smoke lane with explicit runbook

Create a task packet plus a compact smoke runbook and result template. AI workers run the lane locally, update evidence/status docs, and treat failures as the next task.

Pros:

- fastest path to value;
- matches the current AI-first operating layer;
- low implementation risk;
- easy to extend later into scripts or CI.

Cons:

- still relies on local/manual execution;
- not yet a fully automated guardrail.

### Approach 2: CI-first smoke workflow

Add an end-to-end smoke job directly to GitHub Actions now.

Pros:

- strongest automation signal;
- merges could be gated by the demo path earlier.

Cons:

- high flake risk;
- likely needs server boot orchestration and deterministic fixture setup first;
- broadens scope into infrastructure before the lane is stable.

### Approach 3: Runtime-first orchestration

Build a local deployment/dev orchestration layer first, then hang the smoke lane on top.

Pros:

- better long-term foundation for repeated runs.

Cons:

- slows down contest-facing value;
- adds operating complexity before we have a proven smoke contract.

## Recommendation

Choose Approach 1.

It fits the repository’s current maturity: the MVP path exists, evidence exists, and CI exists, but the repo still needs one explicit “demo is alive” lane that an AI worker can execute reliably without inventing staging or fighting flaky browser automation. Once that lane is stable for a few cycles, it can be partially scripted or promoted into CI.

## Proposed Design

### 1. New task packet for the smoke lane

Create a docs/workflow task packet dedicated to demo readiness smoke validation.

That packet should define:

- goal;
- owned files;
- do-not-touch files;
- exact smoke path;
- validation commands;
- pass/fail contract;
- handoff behavior when a stage fails.

This gives the next AI worker an execution contract before any scripting or automation work begins.

### 2. Add a dedicated smoke runbook under `docs/contest/`

Round 1 should add a small runbook, not a giant document set.

The runbook should cover the MVP flow in the same order as the competition story:

1. backend starts;
2. frontend starts or builds successfully;
3. Knowledge Pack metadata is available;
4. assessment generation works with Knowledge Pack context;
5. Tutor workspace answers with Knowledge Pack context;
6. Dashboard shows the recent activity.

For each stage, the runbook should say:

- what command or action to run;
- what visible success condition to expect;
- what evidence file or note to refresh if needed;
- what kind of failure should stop the lane.

### 3. Add a compact smoke result/status entry point

The lane needs a tiny place to record the latest smoke result without bloating the control plane.

The preferred shape is:

- `docs/contest/SMOKE_CHECKLIST.md` or `docs/contest/SMOKE_RUNBOOK.md` for execution;
- `ai_first/EXECUTION_QUEUE.md` for the latest status and next task pointer;
- `ai_first/daily/YYYY-MM-DD.md` for the detailed run record.

The smoke lane should not create another overlapping queue file.

### 4. Failure handling becomes part of the autonomous loop

The lane is only useful if failure behavior is explicit.

Round 1 should define:

- if smoke passes: update evidence/status, then choose the next task from the queue;
- if smoke fails because of product/runtime behavior: create or update a follow-up task packet for the failing area before doing broad new work;
- if smoke fails because of environment or credentials: record the blocker clearly in `EXECUTION_QUEUE.md` and the daily log, and stop pretending the lane is green.

### 5. Keep round 1 light on automation

The first version should not require Playwright, new services, or deployment steps unless existing local tooling already supports them cleanly.

The lane should prefer:

- existing backend startup path;
- existing frontend startup/build path;
- existing contest evidence docs;
- existing status mirrors.

If scripting is useful, it should be a follow-up task after the smoke contract is written and exercised once.

## Files to Introduce or Update in Round 1

Expected docs/workflow surface:

- `docs/superpowers/tasks/2026-04-19-demo-readiness-smoke.md`
- `docs/contest/SMOKE_RUNBOOK.md` or `docs/contest/SMOKE_CHECKLIST.md`
- `docs/superpowers/pr-notes/demo-readiness-smoke-packet.md`
- `ai_first/EXECUTION_QUEUE.md`
- `ai_first/AI_OPERATING_PROMPT.md` only if the queue/operating rules change
- `ai_first/CURRENT_STATE.md`
- `ai_first/NEXT_ACTIONS.md`
- `ai_first/daily/2026-04-19.md`

## Acceptance Criteria

Round 1 is successful when:

1. there is one explicit smoke-lane task packet;
2. there is one compact smoke execution doc for the MVP path;
3. the lane defines clear pass/fail behavior;
4. the AI-first queue points to smoke as the next operating task;
5. the change stays docs/workflow-only.

## Testing and Validation

For the docs/workflow round, validation should stay lightweight:

- `rg -n "smoke|demo readiness|Knowledge Pack|assessment|Tutor|Dashboard|Mermaid" docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first`
- `git diff --check`

Manual review should confirm that a new AI worker can identify:

- the smoke path;
- the stop conditions;
- the next action if the smoke path fails.

## Risks

### Scope creep into infrastructure

If the lane tries to solve deployment, browser automation, and fixture orchestration immediately, it will stall.

Mitigation: keep round 1 docs-first and convert only the proven parts into scripts later.

### Duplicate operating state

If the smoke lane adds yet another queue/status document, the repo drifts again.

Mitigation: keep status in `ai_first/EXECUTION_QUEUE.md` and detailed run history in the daily log.

### False green

If the smoke lane lacks explicit failure handling, AI workers may mark progress without proving the demo path.

Mitigation: make pass/fail and blocker handling part of the written contract.

## Open Questions Resolved for Round 1

- Should smoke be CI-gated immediately? No. Start local/docs-first.
- Should this add deployment or hosting? No.
- Should this create new product code? No.
- Should failure automatically become the next task? Yes.

## Implementation Preview

After this spec is approved, the implementation plan should focus on two small docs/workflow tasks:

1. create the smoke lane packet and supporting docs;
2. update the AI-first queue/status mirrors to make smoke the next operating step.
