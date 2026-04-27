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
