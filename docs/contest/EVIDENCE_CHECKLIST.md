# Evidence Checklist

Use this checklist after running the demo locally.

## Required Screenshots

| Area | Evidence | Status | Notes |
| --- | --- | --- | --- |
| Knowledge Pack | Metadata form filled with demo-safe subject, grade, curriculum, objectives, owner, and sharing status | Pending capture | Use one consistent sample topic. |
| Knowledge Pack | Metadata still visible after reload | Pending capture | Confirms persistence. |
| Assessment | Quiz or assessment configuration using the demo subject or Knowledge Pack | Pending capture | Avoid private source material. |
| Assessment | Generated questions visible | Pending capture | Capture enough context to prove generation worked. |
| Assessment | Common-mistake or feedback guidance visible | Pending capture | Shows learning support, not only question output. |
| Tutor Agent | Student asks a follow-up question | Pending capture | Use a short student-style prompt. |
| Tutor Agent | Tutor response with learning context | Pending capture | Confirm it is demo-safe. |
| Dashboard | Summary cards visible | Pending capture | Include sessions, assessments, tutoring, and running activity. |
| Dashboard | Recent activity includes assessment/tutoring distinction and Knowledge Pack reference | Pending capture | Shows the loop closes for the teacher. |

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

- Video link: Pending.

## Pass/Fail Summary

| Criterion | Status | Notes |
| --- | --- | --- |
| Full MVP story can be followed from docs | Pending final read-through | Start with `docs/contest/README.md`. |
| Product commands have local validation evidence | Passed | See `VALIDATION_REPORT.md`. |
| Screenshots are captured and linked | Pending capture | Requires running local app. |
| Video is captured or explicitly deferred | Pending capture | Optional unless submission requires it. |
| No secrets or private data in evidence | Pending review | Check before publishing. |
