# Spec: F112 Provenance And Reason Trace Surfaces

## Problem

The product already has bounded trust ingredients:

- runtime-policy audit for agent specs
- diagnosis evidence strings
- teacher-review framing on diagnosis and recommendations

But those signals are not surfaced clearly enough in teacher-facing UI. Teachers can see conclusions and actions, yet they cannot quickly inspect why a recommendation exists or which teacher-authored policy slices are actually shaping an agent.

## Decision

Implement three bounded trust surfaces:

1. `Runtime policy audit panel` in `/agents`
   - fetch existing `/api/v1/agent-specs/{agent_id}/runtime-policy-audit`
   - show capability, spec version, applied slices, missing slices, knowledge policy, source priority, and slice sources

2. `Student trust trace` in dashboard detail
   - show diagnosis policy
   - show teacher-review-required framing
   - show structured evidence chips already present in the payload
   - show bounded recommendation rationale and abstain state when present

3. `Small-group reason trace`
   - derive a compact shared reason trace from grouped student payloads
   - show topic, diagnosis type, source action type, confidence tag, and a few real supporting evidence snippets

## Non-goals

- full chain-of-thought exposure
- freeform explainability generation
- changing runtime behavior or diagnosis semantics
- classroom management or roster UX

## File-Level Design

### Backend

- `deeptutor/services/evidence/teacher_insights.py`
  - add bounded `reason_trace` blocks for student and small-group payloads
  - derive them only from existing payload fields

### Frontend

- `web/lib/agent-spec-api.ts`
  - add runtime-policy-audit fetch contract
- `web/components/agents/SpecPackAuthoringTab.tsx`
  - render read-only runtime policy audit panel
- `web/lib/dashboard-api.ts`
  - type the new trust-trace fields
- `web/components/dashboard/StudentInsightDetail.tsx`
  - render a `Trust trace` section
- `web/components/dashboard/StudentInsightCard.tsx`
  - render a compact trust summary
- `web/components/dashboard/SmallGroupInsightCard.tsx`
  - replace generic grouping explanation with bounded reason-trace fields

## Risks

- Overclaiming explainability by adding too much prose.
- Accidentally mixing frontend-only summaries with backend truth.

## Mitigation

- Keep all new trace fields structured and derived.
- Label trust surfaces as bounded evidence and teacher-review context, not proof of correctness.
