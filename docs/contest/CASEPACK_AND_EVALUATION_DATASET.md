# Casepack And Evaluation Dataset

This document explains the structured validation casepack used for contest-safe review and future evaluation work.

## Purpose

The repository now includes a reusable machine-readable casepack at [`../../ai_first/evidence/casepack.json`](../../ai_first/evidence/casepack.json).

Its job is to:

- turn prose-only examples into structured validation scenarios
- keep judge-facing evidence examples consistent across docs
- provide reusable fixtures for later automation work such as `F124`

This is not a benchmark leaderboard, outcome study, or production evaluation harness.

## Categories

The current casepack covers five bounded categories:

- `diagnosis_credibility`
- `recommendation_actionability`
- `abstain_behavior`
- `teacher_execution_loop`
- `trust_trace`

## How Reviewers Should Read It

Each case combines:

- observed evidence signals
- bounded inferred hypothesis
- recommended teacher move when applicable
- teacher-review framing
- one explicit unsafe overclaim the product must avoid

Use the casepack to understand how the current product should be described and validated, not to claim benchmark-grade accuracy.

## Anchor Classroom Case

When a judge or reviewer wants one compact story, reuse the same classroom frame already used in the demo bundle:

- a Grade 9 math teacher prepares `contest-demo-quadratics`
- the learner shows repeated weakness around sign reasoning and factor-pair selection
- the tutor stays grounded in the same pack and gives scaffolded support
- the dashboard helps the teacher review evidence and decide the next reteach move

The casepack exists to keep that narrative bounded and repeatable. It does not convert the story into a measured classroom-outcome claim.

## Bounded Metric Card

Use the following metric set only as an operational evidence card:

| Metric | Current bounded value | Source |
| --- | --- | --- |
| Current demo-safe Knowledge Pack used as the anchor scenario | `contest-demo-quadratics` | [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md) |
| Verified demo-safe sessions carrying the anchor scenario | `2` sessions (`contest-assessment-demo`, `contest-tutor-demo`) | [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md) |
| Teacher-review step in the documented loop | `Present` | [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md), [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md) |
| Claim level | `validated prototype`, not benchmark or classroom outcome proof | [`README.md`](./README.md), [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md) |

Explicit non-claims:

- not diagnosis accuracy
- not student learning gain
- not classroom improvement
- not pilot-scale effectiveness

## How AI Workers Should Reuse It

- use the JSON casepack as the structured source-of-truth
- use contest docs as the narrative layer
- do not invent parallel example sets unless a new task explicitly requires them
- extend the dataset by adding new cases, not by mutating older cases to fit a new story

## Current Limits

- the casepack is a validation asset, not runtime tutoring data
- it does not prove classroom outcomes
- it does not replace teacher review
- it does not justify autonomous diagnosis accuracy claims
