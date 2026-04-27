# F123 Casepack And Evaluation Dataset Expansion Architecture Note

## Summary

`F123` adds a reusable validation casepack for diagnosis credibility and abstain behavior. It does not change product runtime or teacher-facing UX. The pack lives under AI-first evidence assets and is verified against current diagnosis behavior by a lightweight regression-style test.

## Structure

```mermaid
flowchart TD
  CaseStudies["docs/contest/DIAGNOSIS_CASE_STUDIES.md"] --> Casepack["ai_first/evidence/casepacks/diagnosis-validation-pack.json"]
  Tests["tests/services/evidence/test_validation_casepack.py"] --> Casepack
  Tests --> Diagnosis["build_student_diagnosis"]
  ContestReadme["docs/contest/VALIDATION_CASEPACK.md"] --> Casepack
```

## Notes

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated.
- The casepack is a bounded validation artifact, not a benchmark leaderboard.
