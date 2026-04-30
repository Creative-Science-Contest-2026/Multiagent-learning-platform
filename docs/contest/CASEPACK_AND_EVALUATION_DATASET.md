# Casepack And Evaluation Dataset

This document explains the structured validation casepack used for contest-safe review and future evaluation work.

## Purpose

The repository now includes a reusable machine-readable casepack at [`../../ai_first/evidence/casepack.json`](../../ai_first/evidence/casepack.json).

Its job is to:

- turn prose-only examples into structured validation scenarios
- keep judge-facing evidence examples consistent across docs
- provide reusable fixtures for later automation work such as `F124`

This is not a benchmark leaderboard, outcome study, or production evaluation harness.

## Anchor Story Connection

For contest review, do not present the casepack as an abstract testing asset only. Tie it back to the same bounded classroom story used elsewhere in the docs:

- one Grade 9 math Knowledge Pack: `contest-demo-quadratics`
- one weakness pattern around quadratic-equation mistakes
- one teacher review moment on the dashboard
- one bounded classroom move such as a remediation mini-group or scaffolded reteach step

The casepack is the structured support layer for that story, not a separate benchmark track.

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

## Bounded Metric Companion

When presenters need a compact metric card, keep it operational:

| Safe metric type | Why it is allowed here |
| --- | --- |
| count of demo-safe sessions tied to one pack | directly backed by the smoke-validated demo inventory |
| whether the same Knowledge Pack appears across assessment and tutor proof | directly backed by session payloads and dashboard validation |
| whether the recommendation/intervention framing exists | directly backed by the casepack and diagnosis docs |

Do not convert the casepack into:

- accuracy percentages
- learning-gain claims
- autonomous diagnosis rankings
- classroom-effectiveness claims
