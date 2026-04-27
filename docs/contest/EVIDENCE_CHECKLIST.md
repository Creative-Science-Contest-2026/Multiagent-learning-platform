# Evidence Checklist

Use this checklist after running the demo locally.

## Required Screenshots

Refresh these only when the UI changed or when the latest smoke-backed validation marks them stale or blocked.

| Area | Evidence | Refresh mode | Status | Notes |
| --- | --- | --- | --- | --- |
| Knowledge Pack | Metadata form filled with demo-safe subject, grade, curriculum, objectives, owner, and sharing status | Browser capture | Current | Refreshed on 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; see `01-knowledge-pack-metadata.png`. |
| Knowledge Pack | Metadata still visible after reload | Browser capture | Current | Refreshed on 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; see `02-knowledge-pack-after-reload.png`. |
| Assessment | Quiz or assessment configuration using the demo subject or Knowledge Pack | Browser capture | Current | Refreshed on 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; see `04-assessment-config.png`. |
| Assessment | Generated questions visible | Browser capture | Current | Refreshed on 2026-04-25 with demo-safe local session content in the screenshot worktree; see `07-assessment-generated-questions.png`. |
| Assessment | Common-mistake or feedback guidance visible | Browser capture | Current | Refreshed on 2026-04-25 with demo-safe local session content in the screenshot worktree; see `08-assessment-common-mistakes.png`. |
| Tutor Agent | Student asks a follow-up question | Browser capture | Current | Refreshed on 2026-04-25; the student turn is visible in `06-tutor-agent-answer.png`. |
| Tutor Agent | Tutor response with learning context | Browser capture | Current | Refreshed on 2026-04-25; the tutor answer is visible in `06-tutor-agent-answer.png`. |
| Dashboard | Evidence-first teacher insight overview visible | Browser capture | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; see `05-dashboard-evidence-first-overview.png`. |
| Dashboard | Recent activity still visible below the teacher insight workflow | Browser capture | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; see `09-dashboard-recent-activity-evidence-first.png`. |

## Hybrid Proof Screenshots

Use this section to calibrate claims when showing teacher authoring plus evidence loop in one demo.

| Area | Evidence | Refresh mode | Status | Notes |
| --- | --- | --- | --- | --- |
| Agent Specs authoring | Structured `IDENTITY`, `SOUL`, and `RULES` sections visible on `/agents` | Browser capture | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; see `10-agents-spec-pack-authoring.png`. Pair with the bounded runtime-binding test proof when discussing live Tutor behavior. |
| Agent Specs authoring | Export action visible from authoring tab | Browser capture | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; see `11-agents-spec-pack-export.png`. Live runtime impact is now supported by automated bounded proof for the unified Tutor turn path. |

## Required Command Evidence

Refresh these automatically after every successful smoke pass.

Automation source-of-truth for command-backed freshness: `../../ai_first/evidence/evidence_status.json`

| Command | Refresh mode | Status | Source |
| --- | --- | --- | --- |
| `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001` | Auto before smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/system/status` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Auto after smoke | Current | Passed on 2026-04-26; see `VALIDATION_REPORT.md`. |
| `cd web && npm ci && npm run build` | Auto after smoke | Current | Passed on 2026-04-26 in lane 6, with the existing lockfile warning. |

Screenshots and optional video remain manual even when command-backed evidence is refreshed through automation.

## Optional Video

Capture one short video, ideally under five minutes:

1. Knowledge Pack setup.
2. Assessment generation.
3. Student tutoring follow-up.
4. Teacher Dashboard review.
5. Validation report summary.

If capture is required, use [`VIDEO_CAPTURE_RUNBOOK.md`](./VIDEO_CAPTURE_RUNBOOK.md) for the clip order, narration scope, and storage rules.

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
| Hybrid authoring plus evidence-loop claim is calibrated | Passed | Hybrid authoring is documented with bounded runtime-binding proof for the unified Tutor turn path and still avoids universal entry-point claims. |
| Product commands have smoke-backed validation evidence | Passed | See `VALIDATION_REPORT.md`. |
| Screenshots are captured and linked | Passed | Knowledge, assessment, tutor, dashboard, and `/agents` authoring screenshots are current as of the 2026-04-26 recapture run. |
| Video is captured or explicitly deferred | Deferred | Optional unless submission requires it. |
| No secrets or private data in evidence | Passed | Screenshots use demo-safe Knowledge Pack and session data. |
