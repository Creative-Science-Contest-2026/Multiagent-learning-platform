# PR Note: Lane 3 Observation and Student State [L3]

## Summary

This PR extends the Wave 1 evidence spine to capture tutoring observations in runtime and to compute richer student-state rollups with recency-aware summaries.

## Scope

- Added tutoring observation extraction in `deeptutor/services/evidence/extractor.py`.
- Added runtime hook for tutoring observation persistence in `deeptutor/services/session/turn_runtime.py`.
- Extended `student_states` persistence with `recency_summary_json` and rollup computation in `deeptutor/services/session/sqlite_store.py`.
- Added student-state snapshot injection into context history in `deeptutor/services/session/context_builder.py`.
- Added tests for extractor, store rollups, and runtime helper behavior.

## Architecture

```mermaid
flowchart TD
  TurnRuntime[TurnRuntimeManager]\nchat turn completed --> TutoringExtractor[extract_observations_from_tutoring_turn]
  TutoringExtractor --> ObservationTable[(observations)]
  ObservationTable --> Rollup[build_student_state_rollup\nrecency-aware]
  Rollup --> StudentStateTable[(student_states)]
  StudentStateTable --> ContextBuilder[ContextBuilder]
  ContextBuilder --> ChatContext[System snapshot in bounded history]
```

## Contract Notes

- Observation and diagnosis remain separate.
- Raw observations stay queryable from SQLite without requiring diagnosis output.
- Diagnosis rule module (`deeptutor/services/evidence/diagnosis.py`) is unchanged.

## Validation

- `pytest tests/services/evidence/test_extractor.py tests/services/session/test_sqlite_store.py tests/core/test_capabilities_runtime.py -q`
- Scoped `git diff --check` on lane-owned files.

## Main System Map

- Updated: `ai_first/architecture/MAIN_SYSTEM_MAP.md` (evidence extractor/store labels now reflect tutoring capture and recency rollups).
