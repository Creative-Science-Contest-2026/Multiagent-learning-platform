# PR Note: Lane 4 Diagnosis and Recommendation Engine [L4]

## Summary

This lane upgrades diagnosis and recommendation logic from a placeholder rule set to a deterministic hybrid engine with abstain behavior, confidence policy, and ranked actions.

## Scope

- Expanded diagnosis scoring and taxonomy selection in `deeptutor/services/evidence/diagnosis.py`.
- Added deterministic per-student action ranking mapped from diagnosis types.
- Added abstain behavior for weak/contradictory evidence.
- Improved teacher insight grouping to deterministic topic+diagnosis+action cohorts in `deeptutor/services/evidence/teacher_insights.py`.
- Updated assessment/dashboard routers to refresh student-state rollups before diagnosis.
- Added tests for taxonomy routing, confidence tags, abstain behavior, and insights payload structure.

## Architecture

```mermaid
flowchart TD
  Obs[Observed evidence rows] --> Rollup[Student state rollup]
  Rollup --> Dx[Diagnosis engine]
  Dx --> Infer[Inferred hypotheses\n(engine-owned confidence)]
  Infer --> Rank[Deterministic action ranking]
  Rank --> StudentOut[Per-student recommendations]
  StudentOut --> Group[Teacher insight grouper\ntopic+diagnosis+action]
  Group --> SmallGroup[Small-group recommendations]
```

## Contract Notes

- `Observed` remains the source of truth.
- `Inferred` is derived only from observed evidence.
- Confidence tags remain engine-owned (no LLM dependency).
- Action types are mapped explicitly before rationale text.

## Validation

- `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m pytest tests/services/evidence/test_diagnosis.py tests/api/test_assessment_router.py tests/api/test_dashboard_router.py -q`
- `git diff --check` on lane-owned files.

## Main System Map

- Updated: no (logic refinement within existing diagnosis/recommendation pathway).
