# Validation Casepacks

This folder holds reusable, judge-safe validation datasets derived from merged repository behavior.

## Current Pack

- `diagnosis-validation-pack.json`: structured diagnosis and abstain cases anchored to the current `rule_assisted_teacher_review` behavior.

## Usage

- use the pack for regression-style validation and future automation work
- treat it as a bounded validation artifact, not a benchmark leaderboard
- update the source references when a case is added or materially changed

## Rules

- do not fabricate classroom outcomes or benchmark claims
- derive cases from merged docs, tests, or smoke-backed evidence
- keep expected outputs bounded to diagnosis type, abstain code, confidence band, and teacher-review framing
