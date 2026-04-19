# Validation Report

Last updated: 2026-04-19

## Scope

This report covers the current contest MVP path:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

## Evidence Freshness Status

Latest smoke-backed refresh: 2026-04-19

| Evidence group | Refresh mode | Status | Latest source |
| --- | --- | --- | --- |
| Backend and API reachability | Auto after smoke | Current | Smoke run recorded in PR `#24` and `ai_first/daily/2026-04-19.md`. |
| Frontend production build | Auto after smoke | Current | `NEXT_PUBLIC_API_BASE=http://localhost:8001 npm run build` passed during the 2026-04-19 smoke run. |
| Screenshot bundle | Human capture after smoke when the UI changes | Current | Existing contest screenshots still match the smoke-verified MVP path. |
| Optional video | Human capture only | Deferred | No external video is required yet. |

Use these status values consistently:

- `Current`: still matches the latest successful smoke run.
- `Stale`: the MVP path changed after the last successful capture or validation.
- `Blocked`: refresh could not complete because smoke failed or the environment was unavailable.
- `Deferred`: intentionally skipped because the artifact is optional.

## Local Validation Summary

| Area | Command | Result |
| --- | --- | --- |
| Backend health | `curl -s http://127.0.0.1:8001/api/v1/system/status` | Passed in the 2026-04-19 smoke run. |
| Knowledge Pack presence | `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Passed in the 2026-04-19 smoke run; `contest-demo-quadratics` was present with teacher metadata. |
| Dashboard overview | `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Passed in the 2026-04-19 smoke run. |
| Dashboard recent activity | `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Passed in the 2026-04-19 smoke run. |
| Assessment evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Passed in the 2026-04-19 smoke run. |
| Tutor evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Passed in the 2026-04-19 smoke run. |
| Frontend production build | `cd web && NEXT_PUBLIC_API_BASE=http://localhost:8001 npm run build` | Passed in the 2026-04-19 smoke run with the existing lockfile warning. |

## Current Known Limitations

- Screenshot evidence is captured under `docs/contest/screenshots/`.
- Video evidence is deferred unless the final contest submission requires it.
- The frontend build emits a Next.js warning about multiple lockfiles and inferred workspace root. The build still completes successfully.
- Screenshot freshness still requires a human capture step when the UI meaningfully changes.
- Provider-backed AI quality depends on configured model credentials. If credentials are unavailable during a demo, use the command validation and recorded UI flow as fallback evidence.
- This report uses demo-safe descriptions only. Do not add real student data.

## Local Demo Run

The latest smoke-backed evidence refresh used local demo data only:

- Backend: `.venv/bin/python -m deeptutor.api.run_server`
- Frontend validation: `NEXT_PUBLIC_API_BASE=http://localhost:8001 npm run build`
- Knowledge Pack: `contest-demo-quadratics`
- Demo sessions:
  - `contest-assessment-demo`
  - `contest-tutor-demo`

Before future smoke or evidence refresh runs, use `DEMO_DATA_RESET.md` when local demo state may be missing or stale.

The first attempt to run `python3 -m deeptutor.api.run_server` failed because `python3` resolved to a different virtual environment without `uvicorn`. The backend was then run successfully with the repository-local `.venv/bin/python`.

## Smoke-backed Verification Record

The 2026-04-19 smoke run verified the full MVP path in order:

1. backend started successfully with the repository-local virtual environment;
2. system status, knowledge list, dashboard overview, dashboard recent, assessment session, and tutor session endpoints all returned the expected demo-safe data;
3. the frontend production build passed against `http://localhost:8001`;
4. the existing screenshot bundle still matched the smoke-verified flow, so screenshot status remains `Current` instead of requiring immediate recapture.

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
- Screenshot capture refresh: PR `#15`.
- Demo-readiness smoke packet: PR `#23`.
- Demo-readiness smoke execution result: PR `#24`.
- Contest evidence refresh packet: PR `#27`.

## Next Evidence Actions

1. After each successful smoke run, update the evidence freshness table before changing screenshot status.
2. Run `DEMO_DATA_RESET.md` first when demo-safe Knowledge Pack or session data may be stale.
3. Mark screenshots `Stale` or `Blocked` in `EVIDENCE_CHECKLIST.md` only when the smoke result or UI change requires it.
4. Capture and link an external video only if the final submission requires video.
5. Re-run docs validation after evidence docs change:

```bash
rg -n "evidence refresh|smoke|validation|screenshot|video|Current|Stale|Blocked" docs/contest docs/superpowers/tasks docs/superpowers/pr-notes ai_first
git diff --check
```
