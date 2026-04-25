**T050 — Dashboard Insight Depth (PR Note)**

Summary: This PR adds a teacher-facing dashboard insights endpoint (`GET /api/v1/dashboard/insights`) with optional filters (knowledge_base, start_ts, end_ts), TypeScript client bindings, tests, and examples. It contains an initial set of analytics and recommendations derived from session and assessment activity.

Mermaid architecture diagram:

```mermaid
graph LR
  UI[Teachers UI] --> APIClient[web/lib/dashboard-api.ts]
  APIClient --> API[GET /api/v1/dashboard/insights]
  API --> Router[deeptutor.api.routers.dashboard]
  Router --> Store[SessionStore / SQLite]
  Router --> Aggregator[Insights Aggregator (_build_teacher_insights)]
  Aggregator --> Recommendations[Recommendations + Actionable Signals]
```

Checklist:

- [x] Adds filters: `knowledge_base`, `cohort`, `start_ts`, `end_ts`.
- [x] TypeScript client updated to accept filters.
- [x] Unit tests added for filter behavior.
- [x] Local focused tests passed (`tests/api/test_dashboard_router.py`).
- [ ] PR self-review completed; mark Ready for review when approved.

Notes for reviewers:

- The insights endpoint is intentionally lightweight and returns aggregated summary objects; downstream filtering and pagination are available via query params. CI will run the full test matrix.
- See `docs/superpowers/tasks/2026-04-25-T050-dashboard-insight-depth.md` for the task plan and next steps.
