# Task Packet: T010 Assessment Feedback Details

Date: 2026-04-20  
Branch: pod-a/marketplace-pack-import  
Priority: Critical (P2)

## Goal

Enhance assessment review with detailed analysis breakdown, topic-level performance, and actionable recommendations.

## Scope

- Backend: `deeptutor/api/routers/dashboard.py`
  - Add endpoint: `GET /api/v1/dashboard/assessment-analysis/{session_id}`
  - Produce heuristic topic breakdown from question review data
- Frontend API client: `web/lib/dashboard-api.ts`
  - Add `AssessmentAnalysis` types and `getAssessmentAnalysis()`
- Frontend UI:
  - `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
  - `web/components/assessment/ProgressIndicator.tsx`
  - Render topic performance + recommendation lines under recommendations panel
- Tests:
  - `tests/api/test_dashboard_router.py`

## Acceptance Criteria

- Endpoint returns:
  - `summary`
  - `performance_by_topic`
  - `weak_topics`
  - `strong_topics`
  - `recommendations`
- Assessment review page fetches analysis and renders it.
- Existing assessment review flow remains functional.
- Backend syntax and frontend lint checks pass in local environment.

## Validation Notes

- Python compile check: `.venv/bin/python -m py_compile deeptutor/api/routers/dashboard.py`
- Frontend lint check: `npx eslint` on touched files
- API test coverage extended in `tests/api/test_dashboard_router.py`
