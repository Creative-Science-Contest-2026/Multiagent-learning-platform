# T030 Assessment Time Tracking & Analytics

## Summary

- Extended the existing quiz result payload with optional `duration_seconds` so assessment answers can carry lightweight timing data without a new persistence schema.
- Serialized timing into the existing `[Quiz Performance]` transcript and parsed it back in the assessment review service.
- Surfaced total time, average time per question, and optional per-question response time in the assessment review UI.

## Architecture

```mermaid
flowchart LR
  QuizViewer["QuizViewer"] --> SessionAPI["recordQuizResults()"]
  SessionAPI --> QuizResultsRoute["POST /api/v1/sessions/{session_id}/quiz-results"]
  QuizResultsRoute --> Transcript["[Quiz Performance] transcript\noptional ', time: Ns' suffix"]
  Transcript --> ReviewParser["extract_assessment_review()"]
  ReviewParser --> ReviewSummary["summary.estimated_time_spent\nsummary.average_time_per_question"]
  ReviewParser --> ReviewResults["results[].duration_seconds"]
  ReviewSummary --> ReviewPage["/dashboard/assessments/[sessionId]"]
  ReviewResults --> ReviewPage
```

## Notes

- Backward compatibility is preserved for older sessions that do not have timing data.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated for this change.
