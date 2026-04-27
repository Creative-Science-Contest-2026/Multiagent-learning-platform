# F123 Design: Casepack And Evaluation Dataset Expansion

## Goal

Create a reusable validation casepack that turns the current contest-safe diagnosis examples into a structured dataset for future evidence review, UI trust checks, and automation work. This lane stays outside runtime product behavior and focuses on validation assets only.

## Approach

Chosen approach: `docs + machine-readable casepack`.

Why:

- prose-only case studies are useful for judges but weak for regression and reuse
- a full evaluation harness belongs to later automation work such as `F124`
- a lightweight structured casepack gives both human-readable and machine-usable value without widening scope

## Scope

### In scope

- add a machine-readable casepack under `ai_first/evidence/`
- map current diagnosis credibility material into structured cases
- add additional cases for recommendation actionability, abstain behavior, teacher action follow-through, and trust/provenance framing
- document how the casepack should be used in contest review and internal validation
- add a bounded validation check so the dataset shape does not drift silently

### Out of scope

- changing runtime diagnosis logic
- adding new dashboard features
- building a full automated evaluator pipeline
- introducing benchmark claims or accuracy metrics

## Artifact Set

- `ai_first/evidence/casepack.json`
  - source-of-truth dataset
- `docs/contest/CASEPACK_AND_EVALUATION_DATASET.md`
  - human-readable guide
- optional bounded test/helper under `tests/`
  - validates required fields and basic schema shape

## Case Structure

Each case should include:

- `id`
- `category`
- `title`
- `objective`
- `product_surface`
- `observed`
- `inferred`
- `recommended_action`
- `teacher_review_framing`
- `unsafe_overclaim`
- `expected_artifacts`

Recommended categories:

- `diagnosis_credibility`
- `recommendation_actionability`
- `abstain_behavior`
- `teacher_execution_loop`
- `trust_trace`

## Data Flow

1. Existing prose case studies remain useful as judge-facing explanations.
2. The new casepack becomes the structured validation source.
3. Contest docs point to the casepack guide rather than duplicating inconsistent examples.
4. Later automation work can reuse the same dataset instead of inventing new fixtures.

## Validation

- the JSON casepack must parse cleanly
- required fields must be present in every case
- category values should stay inside the bounded list declared by the dataset
- docs references should point to the new casepack guide

## Architecture Impact

- no runtime architecture change
- no `ai_first/architecture/MAIN_SYSTEM_MAP.md` update expected unless a new persistent validation read-path becomes part of the repo-level architecture
