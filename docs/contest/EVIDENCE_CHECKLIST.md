# Evidence Checklist

Use this checklist after running the demo locally.

## Required Screenshots

| Area | Evidence | Status | Notes |
| --- | --- | --- | --- |
| Knowledge Pack | Metadata form filled with demo-safe subject, grade, curriculum, objectives, owner, and sharing status | Captured | [`01-knowledge-pack-metadata.png`](./screenshots/01-knowledge-pack-metadata.png) |
| Knowledge Pack | Metadata still visible after reload | Captured | [`02-knowledge-pack-after-reload.png`](./screenshots/02-knowledge-pack-after-reload.png) |
| Assessment | Quiz or assessment configuration using the demo subject or Knowledge Pack | Captured | [`04-assessment-config.png`](./screenshots/04-assessment-config.png) |
| Assessment | Generated questions visible | Captured | [`07-assessment-generated-questions.png`](./screenshots/07-assessment-generated-questions.png) |
| Assessment | Common-mistake or feedback guidance visible | Captured | [`08-assessment-common-mistakes.png`](./screenshots/08-assessment-common-mistakes.png) |
| Tutor Agent | Student asks a follow-up question | Captured | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Tutor Agent | Tutor response with learning context | Captured | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Dashboard | Summary cards visible | Captured | [`05-dashboard-summary-and-activity.png`](./screenshots/05-dashboard-summary-and-activity.png) |
| Dashboard | Recent activity includes assessment/tutoring distinction and Knowledge Pack reference | Captured | [`05-dashboard-summary-and-activity.png`](./screenshots/05-dashboard-summary-and-activity.png) |

## Required Command Evidence

| Command | Status | Source |
| --- | --- | --- |
| `pytest tests/api/test_knowledge_router.py -v` | Passed in PR `#6` validation | See daily log and PR notes. |
| `pytest tests/knowledge -v` | Passed in PR `#6` validation | See daily log and PR notes. |
| `pytest tests/api/test_question_router.py -v` | Passed in PR `#8` validation | See daily log and PR notes. |
| `pytest tests/api/test_unified_ws_turn_runtime.py -v` | Passed in PR `#8` validation | See daily log and PR notes. |
| `pytest tests/api/test_dashboard_router.py -v` | Passed in PR `#11` validation | See daily log and PR notes. |
| `pytest tests/services/session -v` | Passed in PR `#11` validation | See daily log and PR notes. |
| `python3 -m compileall deeptutor` | Passed in PR `#6`, `#8`, and `#11` validation | See daily log and PR notes. |
| `cd web && npm run build` | Passed in PR `#6`, `#8`, and `#11` validation | Build warns about multiple lockfiles; no build failure. |

## Optional Video

Capture one short video, ideally under five minutes:

1. Knowledge Pack setup.
2. Assessment generation.
3. Student tutoring follow-up.
4. Teacher Dashboard review.
5. Validation report summary.

Store large video files outside the repository and link them here:

- Video link: Deferred. Screenshot evidence is complete; capture and link an external video only if the final contest submission requires it.

## Pass/Fail Summary

| Criterion | Status | Notes |
| --- | --- | --- |
| Full MVP story can be followed from docs | Passed | Start with `docs/contest/README.md`. |
| Product commands have local validation evidence | Passed | See `VALIDATION_REPORT.md`. |
| Screenshots are captured and linked | Passed | See screenshot rows above. |
| Video is captured or explicitly deferred | Deferred | Optional unless submission requires it. |
| No secrets or private data in evidence | Passed | Screenshots use demo-safe Knowledge Pack and session data. |
