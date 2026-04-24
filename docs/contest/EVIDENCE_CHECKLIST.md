# Evidence Checklist

Use this checklist after running the demo locally.

## Required Screenshots

Refresh these only when the UI changed or when the latest smoke-backed validation marks them stale or blocked.

| Area | Evidence | Refresh mode | Status | Notes |
| --- | --- | --- | --- | --- |
| Knowledge Pack | Metadata form filled with demo-safe subject, grade, curriculum, objectives, owner, and sharing status | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Knowledge Pack | Metadata still visible after reload | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Assessment | Quiz or assessment configuration using the demo subject or Knowledge Pack | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Assessment | Generated questions visible | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Assessment | Common-mistake or feedback guidance visible | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Tutor Agent | Student asks a follow-up question | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Tutor Agent | Tutor response with learning context | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Dashboard | Summary cards visible | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |
| Dashboard | Recent activity includes assessment/tutoring distinction and Knowledge Pack reference | Human capture | Stale | Existing capture is still linked, but recent merged UI changes were not followed by a new screenshot pass. |

## Required Command Evidence

Refresh these automatically after every successful smoke pass.

| Command | Refresh mode | Status | Source |
| --- | --- | --- | --- |
| `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001` | Auto before smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/system/status` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Auto after smoke | Current | Passed on 2026-04-24; see `VALIDATION_REPORT.md`. |
| `cd web && npm run build` | Auto after smoke | Current | Passed on 2026-04-24 after `npm ci`, with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local` and the existing lockfile warning. |

## Optional Video

Capture one short video, ideally under five minutes:

1. Knowledge Pack setup.
2. Assessment generation.
3. Student tutoring follow-up.
4. Teacher Dashboard review.
5. Validation report summary.

Store large video files outside the repository and link them here:

- Video link: Deferred. Screenshot evidence is complete; capture and link an external video only if the final contest submission requires it.

Video status follows the same freshness states:

- `Current`: a linked video still matches the latest successful smoke path.
- `Stale`: smoke passed but the flow changed enough that the old video is misleading.
- `Blocked`: smoke failed or no capture environment was available.

## Pass/Fail Summary

| Criterion | Status | Notes |
| --- | --- | --- |
| Full MVP story can be followed from docs | Passed | Start with `docs/contest/README.md`. |
| Product commands have smoke-backed validation evidence | Passed | See `VALIDATION_REPORT.md`. |
| Screenshots are captured and linked | Stale | Existing screenshot links remain available, but a fresh human capture is still required after recent UI merges. |
| Video is captured or explicitly deferred | Deferred | Optional unless submission requires it. |
| No secrets or private data in evidence | Passed | Screenshots use demo-safe Knowledge Pack and session data. |
