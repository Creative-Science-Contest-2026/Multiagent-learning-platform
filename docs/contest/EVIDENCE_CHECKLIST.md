# Evidence Checklist

Use this checklist after running the demo locally.

## Required Screenshots

Refresh these only when the UI changed or when the latest smoke-backed validation marks them stale or blocked.

Recommended judge-view order:

1. `/agents` authoring proof for teacher control
2. Knowledge Pack grounding
3. Assessment generation and feedback
4. Tutor support
5. Dashboard review and next action

| Area | Evidence | Refresh mode | Status | Judge-facing caption | Notes |
| --- | --- | --- | --- | --- | --- |
| Knowledge Pack | Metadata form filled with demo-safe subject, grade, curriculum, objectives, owner, and sharing status | Browser capture | Stale | Teacher sets the trusted learning context before assessment or tutoring begins. | Last real capture was 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; Knowledge page loop framing changed later in PR `#214`, so recapture is required before treating this row as current. |
| Knowledge Pack | Metadata still visible after reload | Browser capture | Stale | The configured classroom context persists after reload rather than living only in one transient form. | Last real capture was 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; Knowledge page loop framing changed later in PR `#214`, so recapture is required before treating this row as current. |
| Assessment | Quiz or assessment configuration using the demo subject or Knowledge Pack | Browser capture | Current | Assessment drafting stays grounded in the same teacher-approved pack. | Refreshed on 2026-04-25 in `docs/t037-contest-screenshot-refresh-pass`; see `04-assessment-config.png`. |
| Assessment | Generated questions visible | Browser capture | Current | The platform can draft practice items from the chosen classroom source. | Refreshed on 2026-04-25 with demo-safe local session content in the screenshot worktree; see `07-assessment-generated-questions.png`. |
| Assessment | Common-mistake or feedback guidance visible | Browser capture | Current | Assessment output includes feedback signals the teacher can reuse or review. | Refreshed on 2026-04-25 with demo-safe local session content in the screenshot worktree; see `08-assessment-common-mistakes.png`. |
| Tutor Agent | Student asks a follow-up question | Browser capture | Stale | The student can continue from assessment into adaptive tutoring on the same topic. | Last real capture was 2026-04-25; Tutor chat framing changed later in PRs `#214` and `#215`, so recapture is required before treating this row as current. |
| Tutor Agent | Tutor response with learning context | Browser capture | Stale | The tutor gives support inside the same classroom loop rather than acting as a final judge. | Last real capture was 2026-04-25; Tutor chat framing changed later in PRs `#214` and `#215`, so recapture is required before treating this row as current. |
| Dashboard | Evidence-first teacher insight overview visible | Browser capture | Stale | The teacher sees reviewed signals and recommended next moves in one operating surface. | Last real capture was 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; dashboard framing changed later in PRs `#214` and `#215`, so recapture is required before treating this row as current. |
| Dashboard | Recent activity still visible below the teacher insight workflow | Browser capture | Stale | The teacher can trace the supporting activity behind the dashboard recommendation layer. | Last real capture was 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; dashboard framing changed later in PRs `#214` and `#215`, so recapture is required before treating this row as current. |

## Hybrid Proof Screenshots

Use this section to calibrate claims when showing teacher authoring plus evidence loop in one demo.

| Area | Evidence | Refresh mode | Status | Judge-facing caption | Notes |
| --- | --- | --- | --- | --- | --- |
| Agent Specs authoring | Structured `IDENTITY`, `SOUL`, and `RULES` sections visible on `/agents` | Browser capture | Stale | Teacher control is explicit: audience, teaching style, and guardrails are configurable before tutoring starts. | Last real capture was 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; `/agents` wording changed later in PR `#215`, so recapture is required before treating this row as current. Pair with the bounded runtime-binding test proof when discussing live Tutor behavior. |
| Agent Specs authoring | Export action visible from authoring tab | Browser capture | Stale | Tutor setup is portable and reviewable as a spec pack rather than hidden prompt state. | Last real capture was 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; `/agents` wording changed later in PR `#215`, so recapture is required before treating this row as current. Live runtime impact is still supported by automated bounded proof for the unified Tutor turn path. |

## Required Command Evidence

Refresh these automatically after every successful smoke pass.

Automation source-of-truth for command-backed freshness: `../../ai_first/evidence/evidence_status.json`

| Command | Refresh mode | Status | Source |
| --- | --- | --- | --- |
| `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001` | Auto before smoke | Current | Passed on 2026-04-28 in Session B; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/system/status` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Auto after smoke | Current | Passed on 2026-04-28; see `VALIDATION_REPORT.md`. |
| `cd web && npm ci && npm run build` | Auto after smoke | Current | Passed on 2026-04-28 in Session B, with the existing lockfile warning. |

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
| Product commands have smoke-backed validation evidence | Passed | Session B refreshed command-backed evidence on 2026-04-28; see `VALIDATION_REPORT.md` and `../../ai_first/evidence/evidence_status.json`. |
| Screenshots are captured and linked | Passed with refresh needed | The linked screenshot bundle still exists, but Knowledge, Tutor, Dashboard, and `/agents` rows are now stale after PRs `#214`, `#215`, and `#216` and should be recaptured before final judge-facing use. |
| Video is captured or explicitly deferred | Deferred | Optional unless submission requires it. |
| No secrets or private data in evidence | Passed | Screenshots use demo-safe Knowledge Pack and session data. |
