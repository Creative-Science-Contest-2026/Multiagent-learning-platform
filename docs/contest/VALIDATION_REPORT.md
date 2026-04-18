# Validation Report

Last updated: 2026-04-19

## Scope

This report covers the current contest MVP path:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Local Validation Summary

| Area | Command | Result |
| --- | --- | --- |
| Knowledge Pack API | `pytest tests/api/test_knowledge_router.py -v` | Passed in PR `#6` validation: 11 passed. |
| Knowledge Pack metadata | `pytest tests/knowledge -v` | Passed in PR `#6` validation: 3 passed. |
| Assessment API | `pytest tests/api/test_question_router.py -v` | Passed in PR `#8` validation: 1 passed. |
| Student tutor runtime contract | `pytest tests/api/test_unified_ws_turn_runtime.py -v` | Passed in PR `#8` validation: 6 passed. |
| Teacher Dashboard API | `pytest tests/api/test_dashboard_router.py -v` | Passed in PR `#11` validation: 2 passed. |
| Session persistence regression | `pytest tests/services/session -v` | Passed in PR `#11` validation: 2 passed. |
| Backend syntax/import sweep | `python3 -m compileall deeptutor` | Passed in PR `#6`, `#8`, and `#11` validation. |
| Frontend production build | `cd web && npm run build` | Passed in PR `#6`, `#8`, and `#11` validation. |

## Current Known Limitations

- Screenshot evidence is captured under `docs/contest/screenshots/`.
- Video evidence is deferred unless the final contest submission requires it.
- The frontend build emits a Next.js warning about multiple lockfiles and inferred workspace root. The build still completes successfully.
- Provider-backed AI quality depends on configured model credentials. If credentials are unavailable during a demo, use the command validation and recorded UI flow as fallback evidence.
- This report uses demo-safe descriptions only. Do not add real student data.

## Local Demo Run

The screenshot capture used local demo data only:

- Backend: `.venv/bin/python -m deeptutor.api.run_server`
- Frontend: `NEXT_PUBLIC_API_BASE=http://localhost:8001 npm run dev`
- Knowledge Pack: `contest-demo-quadratics`
- Demo sessions:
  - `contest-assessment-demo`
  - `contest-tutor-demo`

The first attempt to run `python3 -m deeptutor.api.run_server` failed because `python3` resolved to a different virtual environment without `uvicorn`. The backend was then run successfully with the repository-local `.venv/bin/python`.

## Manual Verification Template

Complete this section when the local app is running.

| Step | Expected result | Status | Evidence link |
| --- | --- | --- | --- |
| Open Knowledge page | Teacher can create or edit Knowledge Pack metadata | Passed | [`01-knowledge-pack-metadata.png`](./screenshots/01-knowledge-pack-metadata.png) |
| Reload Knowledge page | Metadata remains visible | Passed | [`02-knowledge-pack-after-reload.png`](./screenshots/02-knowledge-pack-after-reload.png) |
| Generate assessment | Questions are generated from selected subject/context | Passed with seeded demo result metadata | [`07-assessment-generated-questions.png`](./screenshots/07-assessment-generated-questions.png) |
| Review feedback | Common-mistake or guidance output is visible | Passed | [`08-assessment-common-mistakes.png`](./screenshots/08-assessment-common-mistakes.png) |
| Ask Tutor Agent follow-up | Tutor responds to student question | Passed with seeded demo response | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Open Dashboard | Recent assessment and tutoring activity appears | Passed | [`05-dashboard-summary-and-activity.png`](./screenshots/05-dashboard-summary-and-activity.png) |

## PR Evidence Links

- Knowledge Pack MVP: PR `#6`.
- Assessment and Student Tutor Workspace MVP: PR `#8`.
- Teacher Dashboard MVP: PR `#11`.
- Contest evidence packet: PR `#13`.

## Next Evidence Actions

1. Use these screenshots for the current repo evidence review.
2. Capture and link an external video only if the final submission requires video.
3. Re-run docs validation after evidence docs change:

```bash
rg -n "Knowledge Pack|assessment|Tutor|Dashboard|Mermaid|validation|screenshot|video" docs/contest docs/superpowers/pr-notes
git diff --check
```
