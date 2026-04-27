# F116 Student Model Enrichment Design

## Metadata

- Task ID: `F116_STUDENT_MODEL_ENRICHMENT`
- Commit tag: `F116`
- Session bucket: `session-b-runtime-data`
- Owner scope: `deeptutor/services/evidence/`, `deeptutor/services/session/`, bounded tests/docs
- Do-not-touch scope: teacher-facing dashboard UX, `/agents` UX, unrelated runtime-policy surfaces

## Goal

Enrich the existing student-state contract so diagnosis and future teacher-trust work can use more than repeated mistakes, support level, and confidence trend, while still staying grounded in observed evidence.

## Current State

- student state currently stores `repeated_mistakes`, `support_level`, `confidence_trend`, and a `recency_summary`
- rollups are derived from recent observations in `SQLiteSessionStore`
- diagnosis uses student state only as bounded context and falls back to a tiny derived state when nothing is persisted
- there is no structured place for topic-specific mastery signals, misconception persistence, or support-pattern summaries beyond the current thin rollup

## Problem

The current student model is useful but shallow. Later tasks like confidence calibration, taxonomy expansion, and intervention effectiveness need richer context than:

- a short repeated-mistakes list
- one coarse support label
- one confidence trend

Without richer but still inspectable signals, later features will either duplicate rollup logic in multiple places or drift toward ad hoc heuristics.

## Recommended Approach

Extend the student-state record with additive, evidence-backed substructures such as:

- `mastery_signals`
- `support_signals`
- `misconception_signals`

These should be derived directly from observed assessment/tutoring behavior and stored alongside the existing fields, not replace them.

## Proposed Contract

Keep the current top-level fields and add nested dictionaries:

```json
{
  "student_id": "student-a",
  "repeated_mistakes": ["fractions", "equations"],
  "support_level": "guided",
  "confidence_trend": "down",
  "recency_summary": {...},
  "mastery_signals": {
    "emerging_topics": ["fractions"],
    "stable_topics": [],
    "at_risk_topics": ["equations"]
  },
  "support_signals": {
    "heavy_hint_topics": ["fractions"],
    "retry_heavy_topics": ["equations"],
    "recent_support_burden": "elevated"
  },
  "misconception_signals": {
    "dominant_errors": {
      "fractions": "concept_gap"
    },
    "persistent_topics": ["fractions"]
  }
}
```

## Design Notes

### 1. Derive, Don’t Invent

Every new field must map back to observed rows or the existing diagnosis taxonomy. Avoid synthetic scores that cannot be explained from recorded evidence.

### 2. Keep Diagnosis Observation-First

Diagnosis should continue to score from observations first. The enriched student state is context that can sharpen teacher-readable summaries and later ranking, not a replacement inference engine.

### 3. Prefer Topic Buckets Over Global Scores

Topic-level buckets like `at_risk_topics` or `heavy_hint_topics` are easier to audit and safer than compressing a student into one numeric mastery score.

### 4. Preserve Compatibility

Existing readers that only use `repeated_mistakes`, `support_level`, `confidence_trend`, and `recency_summary` should continue to work unchanged.

## Testing Strategy

- session-store tests for richer rollup output
- evidence/diagnosis tests proving enriched state is preserved and remains bounded
- bounded API test updates only if an existing backend payload materially changes shape

## Success Criteria

1. student state persists richer mastery/support/misconception substructures
2. rollup logic stays explainable from observations
3. existing diagnosis behavior remains observation-first and compatible
4. no teacher-facing dashboard presentation files are modified
