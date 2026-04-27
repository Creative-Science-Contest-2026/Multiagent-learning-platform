# F120 Design: Intervention Effectiveness Tracking

## Problem

The current teacher insight flow records whether a recommendation was acknowledged, turned into a teacher action, or converted into an intervention assignment, but it does not summarize what happened after that intervention. Teachers can inspect history, yet the system cannot surface a bounded answer to the practical question: did the later evidence appear to improve, stay unclear, or worsen after the intervention?

## Design Direction

Keep this slice observational. The system should not claim that an intervention caused a later improvement. Instead, it should compute a small effectiveness summary from:

- the intervention record itself
- the targeted student or group/topic
- later observations on the same topic
- recency and confidence constraints already established by `F117` and `F119`

Recommended summary labels:

- `appears_helpful`
- `mixed_or_unclear`
- `no_followup_signal`

## Proposed Contract

1. Add a focused helper in `deeptutor/services/evidence/` that evaluates post-intervention evidence windows against existing intervention history records.
2. Treat recommendation acknowledgements, teacher actions, and intervention assignments as potential intervention anchors, but only score effectiveness when later observations exist on the same student/topic or small-group topic.
3. Keep the summary bounded:
   - label
   - supporting reason text
   - counts or timestamps used
4. Attach the summary only to existing teacher-insight payloads where it naturally fits, such as student `intervention_history` rows or small-group records.

## Approach Options

### Option A — History-only badges

Show whether an intervention was followed by later observations, without judging direction.

Pros:
- lowest risk

Cons:
- weak teacher value

### Option B — Observational outcome summaries

Compare later evidence on the same topic and emit a bounded label like `appears_helpful`, `mixed_or_unclear`, or `no_followup_signal`.

Pros:
- useful signal without overclaiming
- fits current evidence architecture

Cons:
- needs explicit windowing and topic matching rules

### Option C — Intervention scoring model

Compute numeric success scores across interventions.

Pros:
- more compact ranking

Cons:
- too close to causal claims
- exceeds bounded-proof scope

## Recommendation

Use **Option B**. It gives a meaningful teacher-facing signal while staying inside the evidence-first, non-causal framing the current product can defend.

## Scope Boundary

- in scope: evidence-layer effectiveness helper, bounded payload additions, dashboard API proof
- out of scope: new UI widgets, causal modeling, experiment infrastructure, or roster/classroom ownership changes

## Proof Plan

- service tests prove labels for helpful, unclear, and no-followup cases
- dashboard API tests prove the summary attaches to existing payload structures without changing presentation contracts
- PR note documents the observational boundary explicitly
