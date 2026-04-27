# Diagnosis Credibility Case Studies

Use these cases when a reviewer asks how the diagnosis layer works or how much trust to place in it.

Structured source-of-truth: the reusable machine-readable pack now lives at [`../../ai_first/evidence/casepack.json`](../../ai_first/evidence/casepack.json). This document remains the judge-facing prose layer for a subset of those cases.

## Framing

- The diagnosis layer is `rule_assisted_teacher_review`, not a benchmarked autonomous assessor.
- Each diagnosis is a teacher-reviewable hypothesis built from observed signals.
- When evidence is too weak or mixed, the system abstains instead of overstating certainty.

## Case 1: Concept Gap In Fraction Subtraction

**Observed**

- Topic: `fractions subtraction`
- Two incorrect answers in the same topic
- Long response times: `48s`, `61s`
- Retry behavior present

**Inferred**

- Diagnosis: `concept_gap`
- Confidence: `medium` to `high`
- Why:
  - repeated misses on one topic
  - slow responses
  - retry pattern suggests misunderstanding, not just carelessness

**Recommended action**

- `review_prerequisite`

**Teacher review framing**

- Safe claim: the system is highlighting a likely prerequisite gap worth checking.
- Unsafe claim: the system has proven the student's exact misconception without teacher review.

## Case 2: Careless Error In Basic Arithmetic

**Observed**

- Topic: `arithmetic`
- Two incorrect answers
- Very short response times: `8s`, `10s`
- No strong hint or retry pattern

**Inferred**

- Diagnosis: `careless_error`
- Confidence: bounded by the rule pattern, not by external benchmark accuracy
- Why:
  - errors happen quickly
  - low support load
  - pattern looks more like haste than a deep conceptual gap

**Recommended action**

- `retry_easier`

**Teacher review framing**

- Safe claim: the student may need a quick accuracy-reset loop.
- Unsafe claim: the system has ruled out all conceptual confusion.

## Case 3: Abstain On Strong Correct Signal

**Observed**

- Topic: `geometry`
- Correct answer
- No hint burden
- No retry burden

**Inferred**

- No diagnosis returned
- `abstain_reason`: evidence is too weak or too mixed for a confident diagnosis

**Recommended action**

- None

**Teacher review framing**

- This is a credibility feature, not a weakness.
- The system avoids fabricating intervention when the observation layer does not justify it.

## Judge-Facing Answer

If asked about diagnosis accuracy, use this wording:

> We do not present this as a benchmarked autonomous assessor. It is a rule-assisted, confidence-tagged, teacher-reviewed hypothesis layer. Each recommendation is traceable to observed signals, and weak evidence leads to abstention rather than overclaiming.
