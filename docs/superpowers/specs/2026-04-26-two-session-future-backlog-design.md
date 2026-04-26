# Two-Session Future Backlog Design

Date: 2026-04-26
Status: Proposed

## Goal

Extend the AI-first task system with a long-range backlog of post-contest product work that reflects what the repository still lacks or only implements partially, while keeping the backlog immediately usable for two parallel AI sessions.

The backlog should:
- add 20+ new machine-readable tasks to `ai_first/TASK_REGISTRY.json`
- preserve the existing contest MVP and risk-hardening history
- make dependencies explicit so future AI workers do not guess execution order
- map every new task into one of two recommended execution buckets
- remain honest about current proof level and avoid reopening already-merged contest lanes

## Why A New Backlog Slice Is Needed

The repository now sits in a terminal contest-ready state. The mainline product already covers the contest MVP flow, risk-hardening lanes, and claim calibration. That does not mean the product is complete. Several important capabilities are still missing entirely or exist only as thin MVP slices:
- teacher action execution after insight generation
- intervention outcome tracking
- fuller teacher feedback loops on diagnosis and recommendation quality
- broader runtime/spec coverage and auditability
- deeper learner modeling and grouping operations
- class-level operating surfaces beyond a contest demo dashboard

Without a new backlog slice, future AI workers will either invent ad hoc tasks or reopen merged lanes incorrectly.

## Backlog Strategy

Use a `session-bucketed layered backlog`.

Each new task remains an individual registry entry, but also carries two coordination hints:
- `recommended_session_bucket`
- `layer`

This keeps the registry machine-readable while letting humans and AI workers open only two sessions at a time without losing dependency structure.

## Naming Scheme

Use a new `F` range for future product-expansion tasks:
- `F101` onward

This avoids collision with:
- `T0xx` contest MVP tasks
- `R1-R6` risk-hardening tasks
- `L1-L6` roadmap lanes

Recommended ID format:
- `F101_TEACHER_ACTION_EXECUTION_LOOP`
- `F102_INTERVENTION_ASSIGNMENT_FLOW`

## Registry Contract Additions

Every new future task should include the existing registry fields plus:
- `recommended_session_bucket`
- `layer`

Allowed `recommended_session_bucket` values:
- `session-a-teacher-facing`
- `session-b-runtime-data`

Allowed `layer` values for this backlog slice:
- `teacher-workflow`
- `teacher-insight`
- `teacher-quality-control`
- `runtime-policy`
- `student-model`
- `validation-ops`

These fields are coordination hints, not substitutes for `dependencies`.

## Two-Session Operating Model

### Session A — Teacher-Facing Workflow

Owns work that changes what teachers directly see, approve, execute, or review.

Primary layers:
- `teacher-workflow`
- `teacher-insight`
- `teacher-quality-control`

Typical outputs:
- dashboard actions
- remediation flows
- review controls
- feedback capture
- grouping management
- class queue surfaces

### Session B — Runtime, Evidence, And Data Contracts

Owns work that deepens policy enforcement, student-state quality, recommendation quality, validation evidence, and operational data contracts.

Primary layers:
- `runtime-policy`
- `student-model`
- `validation-ops`

Typical outputs:
- broader runtime binding
- spec version pinning
- student model enrichment
- intervention outcome measurements
- evidence datasets
- pilot feedback ingestion scaffolding

## Dependency Rules

Use registry task IDs in `dependencies`.

Rules:
- only record hard blockers in `dependencies`
- if a task benefits from another task but is still independently startable, record that in `notes` instead
- prefer a shallow dependency graph over chaining every adjacent improvement
- let session bucketing suggest likely parallelism, but do not encode parallelism as a fake dependency

## Proposed Future Task Set

### Session A — Teacher-Facing Workflow

1. `F101_TEACHER_ACTION_EXECUTION_LOOP`
- layer: `teacher-workflow`
- depends on: `R5_DASHBOARD_ACTIONABILITY`
- purpose: turn dashboard recommendations into actionable teacher moves with explicit execution affordances

2. `F102_INTERVENTION_ASSIGNMENT_FLOW`
- layer: `teacher-workflow`
- depends on: `F101_TEACHER_ACTION_EXECUTION_LOOP`
- purpose: let teachers convert a recommendation into a follow-up activity, remediation assignment, or next-step task

3. `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- layer: `teacher-workflow`
- depends on: `F101_TEACHER_ACTION_EXECUTION_LOOP`
- purpose: track whether a teacher accepted, deferred, dismissed, or completed a recommendation

4. `F104_SMALL_GROUP_MANAGEMENT_SURFACE`
- layer: `teacher-workflow`
- depends on: `R5_DASHBOARD_ACTIONABILITY`
- purpose: move from suggested small groups to teacher-managed group objects and actions

5. `F105_CLASS_INTERVENTION_QUEUE`
- layer: `teacher-insight`
- depends on: `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- purpose: show an ordered queue of unresolved teacher actions across students and groups

6. `F106_STUDENT_INSIGHT_TIMELINE`
- layer: `teacher-insight`
- depends on: `R5_DASHBOARD_ACTIONABILITY`
- purpose: deepen student detail with an evidence timeline rather than a single snapshot

7. `F107_INTERVENTION_HISTORY_VIEW`
- layer: `teacher-insight`
- depends on: `F102_INTERVENTION_ASSIGNMENT_FLOW`
- purpose: let teachers inspect what interventions were previously attempted and what happened next

8. `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
- layer: `teacher-quality-control`
- depends on: `R2_DIAGNOSIS_CREDIBILITY`
- purpose: capture teacher feedback on whether a diagnosis was helpful, wrong, or incomplete

9. `F109_RECOMMENDATION_FEEDBACK_CAPTURE`
- layer: `teacher-quality-control`
- depends on: `F103_RECOMMENDATION_ACKNOWLEDGEMENT_AND_STATUS`
- purpose: capture whether recommended teacher moves were practical and relevant

10. `F110_TEACHER_OVERRIDE_LOG`
- layer: `teacher-quality-control`
- depends on: `F108_DIAGNOSIS_FEEDBACK_CAPTURE`
- purpose: record when teachers override AI framing or choose a different pedagogical action

11. `F111_ASSESSMENT_REVIEW_RUBRIC_CONTROLS`
- layer: `teacher-quality-control`
- depends on: `R3_ASSESSMENT_SAFETY`
- purpose: strengthen the teacher review step with structured rubric controls instead of generic approval only

12. `F112_PROVENANCE_AND_REASON_TRACE_SURFACES`
- layer: `teacher-quality-control`
- depends on: `R1_RUNTIME_BINDING_PROOF`, `R2_DIAGNOSIS_CREDIBILITY`
- purpose: expose bounded provenance and rationale trace for teacher-facing trust without overclaiming full explainability

### Session B — Runtime, Evidence, And Data Contracts

13. `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`
- layer: `runtime-policy`
- depends on: `R1_RUNTIME_BINDING_PROOF`
- purpose: extend bounded runtime-binding proof beyond the currently verified Tutor path

14. `F114_SPEC_VERSION_PINNING_PER_SESSION`
- layer: `runtime-policy`
- depends on: `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`
- purpose: pin each learning session to the exact teacher-spec version used at runtime

15. `F115_RUNTIME_POLICY_AUDIT_TRACE`
- layer: `runtime-policy`
- depends on: `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`
- purpose: provide inspectable runtime policy slices for debugging and trust audits

16. `F116_STUDENT_MODEL_ENRICHMENT`
- layer: `student-model`
- depends on: `R2_DIAGNOSIS_CREDIBILITY`
- purpose: expand student state beyond thin recency summaries into richer mastery, support, and misconception fields

17. `F117_CONFIDENCE_CALIBRATION_REFINEMENT`
- layer: `student-model`
- depends on: `F116_STUDENT_MODEL_ENRICHMENT`
- purpose: make confidence tags more stable and better tied to observed evidence density

18. `F118_MISCONCEPTION_TAXONOMY_EXPANSION`
- layer: `student-model`
- depends on: `F116_STUDENT_MODEL_ENRICHMENT`
- purpose: grow diagnosis categories beyond the current narrow MVP taxonomy

19. `F119_ABSTAIN_AND_WEAK_EVIDENCE_REFINEMENT`
- layer: `student-model`
- depends on: `R2_DIAGNOSIS_CREDIBILITY`
- purpose: improve the system's ability to hold back recommendations when evidence is too thin or conflicting

20. `F120_INTERVENTION_EFFECTIVENESS_TRACKING`
- layer: `student-model`
- depends on: `F102_INTERVENTION_ASSIGNMENT_FLOW`, `F116_STUDENT_MODEL_ENRICHMENT`
- purpose: measure whether interventions appear to help and feed that back into teacher insight quality

21. `F121_CLASS_ROSTER_AND_GROUP_FOUNDATION`
- layer: `validation-ops`
- depends on: none
- purpose: add minimal class roster and class ownership primitives needed for true classroom workflows

22. `F122_PILOT_FEEDBACK_INGESTION_PATH`
- layer: `validation-ops`
- depends on: `R6_CLAIM_CALIBRATION_PILOT`
- purpose: prepare a bounded place to store future external walkthrough or pilot feedback honestly

23. `F123_CASEPACK_AND_EVALUATION_DATASET_EXPANSION`
- layer: `validation-ops`
- depends on: `R2_DIAGNOSIS_CREDIBILITY`
- purpose: grow judge-safe case studies into a reusable validation pack for future model and UI checks

24. `F124_EVIDENCE_AUTOMATION_REFRESH`
- layer: `validation-ops`
- depends on: `F123_CASEPACK_AND_EVALUATION_DATASET_EXPANSION`
- purpose: automate more of the smoke, screenshot, and evidence-refresh path so the validated-prototype claim stays easier to maintain

## Execution Recommendation

### Now

Recommended first tasks if only two sessions are open:
- Session A: `F101_TEACHER_ACTION_EXECUTION_LOOP`
- Session B: `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`

These two tasks open the strongest next layer of real product depth with limited cross-session conflict.

### Next

After those complete:
- Session A should move into `F102`, `F103`, `F108`
- Session B should move into `F114`, `F116`, `F119`

### Later

Use the later set once the product starts behaving more like a classroom workflow than a contest demo:
- `F105`, `F107`, `F110`, `F111`, `F112`, `F117`, `F118`, `F120`, `F121`, `F122`, `F123`, `F124`

## Required Repository Changes In The Follow-Up Implementation Plan

The follow-up implementation plan for this docs-only change should:
1. append the new `F101-F124` tasks to `ai_first/TASK_REGISTRY.json`
2. update registry counters and metadata
3. add a short task packet that explains the two-session bucket model and the recommended startup order
4. update `ai_first/ACTIVE_ASSIGNMENTS.md` and the daily log only as needed for this docs lane
5. avoid reopening or rewriting completed contest MVP and risk-hardening entries

## Non-Goals

This backlog extension does not:
- start implementation of the future tasks themselves
- redefine the finished contest MVP or risk-hardening lanes
- claim that the repository already supports real pilot workflows or full classroom operations
- change the current terminal status that no AI implementation task is active until a fresh packet is opened
