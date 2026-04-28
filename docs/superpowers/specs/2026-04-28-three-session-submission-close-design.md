# Three-Session Submission Close Design

Date: 2026-04-28
Status: Draft for user review
Scope: Final contest-submission closing backlog for the current product state

## Goal

Define a final AI-first execution design that turns the current repository state into a submission-ready package for the VnExpress Sáng kiến Khoa học 2026 contest.

The backlog must:

- cover product proof, demo data, evidence, docs, narrative, and submission packaging;
- include already-merged capabilities when they still require review, revalidation, recapture, or packaging;
- be decomposed into small PR-sized tasks;
- support three concurrent AI sessions with minimal file conflicts;
- preserve a hard split between:
  - Phase 1: enough to submit confidently;
  - Phase 2: optional polish if time remains.

## Product framing

The submission should not position the repository as "DeepTutor with more features."

The submission should position the product as:

> A teacher-controlled adaptive tutor for Vietnamese classrooms.

The core product loop to preserve across docs, evidence, and demo flow is:

`Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`

Everything in the final backlog should strengthen that loop, validate that loop, or package that loop for contest review.

## Constraints

- Follow `AGENTS.md` and `ai_first/AI_OPERATING_PROMPT.md`.
- Respect the current AI-first control plane and contest evidence structure.
- Do not invent a second queue, second evidence tree, or second submission narrative.
- Use current `main` as the product baseline.
- Treat already-merged features as implementation-complete unless validation proves otherwise.
- Prefer docs, validation, evidence, and packaging tasks over new runtime feature work.
- Only create runtime fix PRs when a validation task finds a concrete submission blocker.

## Non-goals

- No broad new feature expansion.
- No repo-wide refactor for cleanliness alone.
- No attempt to resell every inherited DeepTutor capability as contest scope.
- No large UI redesign that risks destabilizing the submission package.

## Execution model

The work is organized as small PR-sized tasks, but coordinated through two phases:

### Phase 1: Submit confidently

Phase 1 ends when the repository contains one clear read path for submission, current evidence, validated claims, demo-safe operating instructions, and explicit manual review gates.

After Phase 1, the team should be able to submit without re-reading old chats or rediscovering repository context.

### Phase 2: Optional polish

Phase 2 includes only work that increases clarity, differentiation, or presentation quality without becoming a hidden dependency for submission readiness.

If time runs short, all Phase 2 work can be dropped without losing the ability to submit.

## PR backlog

### Phase 1 PRs

1. `PR-CLOSE-01 Submission Scope Freeze`
   Lock the official contest scope around the teacher-controlled adaptive tutoring loop and explicitly mark non-core features as secondary or out of demo scope.

2. `PR-CLOSE-02 Claim and Proof Contract Freeze`
   Build a claim-to-evidence contract so product wording, validation wording, and contest wording stay aligned and do not overclaim.

3. `PR-CLOSE-03 Core Loop Runtime Revalidation`
   Re-check the current `main` behavior for the five-step product loop and record any real blockers that require a separate fix PR.

4. `PR-CLOSE-04 Demo Data and Smoke Contract Refresh`
   Reconfirm the demo-safe dataset, reset flow, smoke order, and manual checks needed to reproduce the contest path.

5. `PR-CLOSE-05 Evidence Bundle Refresh`
   Re-index and refresh screenshots, evidence notes, and artifact statuses so each required submission asset is clearly current, pending human capture, or optional.

6. `PR-CLOSE-06 Submission Narrative Pack`
   Finalize the contest-ready product description, differentiation framing, and fork-transparency wording around the validated prototype scope.

7. `PR-CLOSE-07 Submission Operator Pack`
   Create the final operator-facing entrypoint that tells a human exactly what to read, what to attach, and what to verify before submitting.

8. `PR-CLOSE-08 Human Review Gates`
   Convert remaining manual-only work into explicit gates with owners and statuses, including IP review, optional video decision, wording review, and final sign-off.

9. `PR-CLOSE-09 Final Package Readiness`
   Run the last consistency pass across artifacts and declare the package ready only when all required paths, docs, and manual gates are visible and coherent.

### Phase 2 PRs

10. `PR-POLISH-01 Teacher-First Entry Polish`
    Improve the first impression so the product immediately reads as teacher-controlled classroom software rather than a generic AI workspace.

11. `PR-POLISH-02 Core Loop Visibility Polish`
    Increase the visibility of the five-step loop across existing screens with bounded UX and wording improvements.

12. `PR-POLISH-03 Differentiation Wording Sweep`
    Align contest-facing product copy with the submission narrative so the app itself reinforces the same product story.

13. `PR-POLISH-04 Judge-Facing Visual Asset Polish`
    Improve screenshot selection, captions, and supporting visual presentation for judges.

14. `PR-POLISH-05 Post-Polish Evidence Recapture`
    Re-run the limited evidence refresh needed after any Phase 2 product or wording polish.

## Three-session parallelization design

The user intends to run three AI sessions in parallel. The primary optimization target is minimal file conflict, not maximum theoretical throughput.

To achieve that, session boundaries should be defined by write zones first and by task theme second.

### Session A: Narrative and submission skeleton

Primary goal:
Own the final submission story and packaging skeleton without waiting on every validation artifact to finish.

Preferred PR ownership:

- `PR-CLOSE-01 Submission Scope Freeze`
- the submission-facing parts of `PR-CLOSE-06 Submission Narrative Pack`
- the skeleton of `PR-CLOSE-07 Submission Operator Pack`
- the checklist structure of `PR-CLOSE-08 Human Review Gates`

Primary write zone:

- `ai_first/competition/*`
- `docs/contest/README.md`
- final submission entrypoint or final runbook
- summary docs that define "what this product is"

Rules:

- Session A is the source of truth for product framing and submission wording.
- Session A should avoid editing validation-heavy files owned by Session B unless a handoff is explicit.
- Session A can reserve reference slots for evidence links, but should not invent evidence status.

### Session B: Validation, smoke, and evidence

Primary goal:
Own the proof that current `main` supports the contest path and keep evidence freshness accurate.

Preferred PR ownership:

- `PR-CLOSE-03 Core Loop Runtime Revalidation`
- `PR-CLOSE-04 Demo Data and Smoke Contract Refresh`
- most of `PR-CLOSE-05 Evidence Bundle Refresh`
- `PR-POLISH-05 Post-Polish Evidence Recapture` if Phase 2 happens

Primary write zone:

- `docs/contest/VALIDATION_REPORT.md`
- `docs/contest/SMOKE_RUNBOOK.md`
- `docs/contest/DEMO_DATA_RESET.md`
- `docs/contest/EVIDENCE_CHECKLIST.md`
- `ai_first/evidence/*`

Rules:

- Session B is the source of truth for validation status and evidence freshness.
- Session B should not redefine product scope or contest claims; it validates against Session A's contract.
- If Session B finds a real product blocker, it should open or request a narrow fix PR instead of hiding the issue in docs.

### Session C: Runtime fixes and optional polish

Primary goal:
Absorb any narrow runtime mismatch found by Session B and later take Phase 2 product polish tasks with minimal contention.

Preferred PR ownership:

- any small runtime fix PR discovered during `PR-CLOSE-03`
- `PR-POLISH-01 Teacher-First Entry Polish`
- `PR-POLISH-02 Core Loop Visibility Polish`
- `PR-POLISH-03 Differentiation Wording Sweep`
- product-facing parts of `PR-POLISH-04 Judge-Facing Visual Asset Polish`

Primary write zone:

- contest-facing product screens
- app wording surfaces
- small demo-path runtime fixes

Rules:

- Session C should stay idle or in analysis mode until a concrete fix or polish target exists.
- Session C does not create new product claims.
- Session C does not rewrite the submission package; it keeps product surfaces consistent with the narrative already frozen by Session A.

## Conflict-minimizing allocation rules

Because the optimization target is minimal file conflict, the following write-boundary rules apply:

1. `docs/contest/README.md` should be owned by Session A.
2. Validation artifacts under `docs/contest/VALIDATION_REPORT.md`, `SMOKE_RUNBOOK.md`, `DEMO_DATA_RESET.md`, and `EVIDENCE_CHECKLIST.md` should be owned by Session B.
3. Product-facing app files should be owned by Session C when a runtime fix or polish is required.
4. If a task touches both narrative and validation files, split it into two PRs rather than forcing joint ownership.
5. If a task touches both evidence docs and product files, Session B should record the blocker and Session C should own the fix PR.
6. Session A and Session B should not both actively edit the same contest doc in the same wave unless one session is only providing review comments.

## Ordering and dependency model

Some tasks can start in parallel, but not all.

### Can start immediately in parallel

- Session A: `PR-CLOSE-01`
- Session B: `PR-CLOSE-03`
- Session C: prepare to absorb runtime fixes or pre-scope Phase 2 surfaces without editing shared docs

### Must wait for scope and claim stabilization

- `PR-CLOSE-02` should follow `PR-CLOSE-01`
- the final wording in `PR-CLOSE-06` should follow `PR-CLOSE-01` and materially align with `PR-CLOSE-02`
- evidence wording in Session B should align with the claim contract once it exists

### Must wait for validation outputs

- `PR-CLOSE-05` depends on current validation status from `PR-CLOSE-03` and `PR-CLOSE-04`
- `PR-CLOSE-09` depends on the outputs of `PR-CLOSE-05`, `PR-CLOSE-07`, and `PR-CLOSE-08`
- `PR-POLISH-05` only exists if Phase 2 changes any submission-relevant visual or wording artifact

## Runtime fix rule

If validation reveals a real blocker in the contest path:

- open one narrow fix PR;
- keep the fix isolated to the broken step;
- do not hide the breakage under wording changes;
- re-run only the affected validation and evidence updates before continuing.

Runtime fix PRs are not part of the base 14-PR plan unless validation proves they are necessary.

## Done definition

The design is successful when:

- the final backlog is decomposed into small PR-sized tasks;
- Phase 1 completion implies the team can submit without rediscovering context;
- Phase 2 is strictly optional;
- three parallel AI sessions can run with low file collision risk;
- product framing, evidence, and packaging all reinforce the same teacher-controlled tutor loop.

## Risks and mitigations

### Risk: three sessions drift into different product stories

Mitigation:
Freeze scope first and treat Session A wording as the narrative source of truth.

### Risk: evidence gets refreshed against stale claims

Mitigation:
Session B validates current behavior, but aligns wording only after the claim contract is frozen.

### Risk: Session C starts polishing before Phase 1 is safe

Mitigation:
Do not start Phase 2 edits until the package is close to `PR-CLOSE-09`, unless Session C is handling a real blocker fix.

### Risk: shared contest docs create merge churn

Mitigation:
Use explicit file ownership and split mixed tasks into separate PRs instead of shared writes.

## Recommended next step

After the user reviews this spec, create the implementation plan as a three-session execution plan with:

- branch and worktree recommendations;
- per-session task packets;
- owned-file contracts;
- dependency edges between sessions;
- merge order for Phase 1 and the optional gate into Phase 2.
