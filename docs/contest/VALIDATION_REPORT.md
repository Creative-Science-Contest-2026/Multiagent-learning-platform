# Validation Report

Last updated: 2026-04-26

## Scope

This report covers the current contest MVP path:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

This report validates prototype behavior and contest evidence only. It is not a classroom outcome study or deployment report.

## Evidence Freshness Status

Latest smoke-backed refresh: 2026-04-26

| Evidence group | Refresh mode | Status | Latest source |
| --- | --- | --- | --- |
| Backend and API reachability | Auto after smoke | Current | Scripted-reset smoke run recorded in `ai_first/daily/2026-04-26.md`. |
| Frontend production build | Auto after smoke | Current | `npm ci && npm run build` passed on 2026-04-26 with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local` in the lane-6 worktree. |
| Screenshot bundle | Browser capture after smoke when the UI changes | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`, including the Lane 5 evidence-first dashboard workflow. |
| Hybrid authoring screenshots (`/agents`) | Browser capture after smoke when hybrid story is presented | Current | Refreshed on 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; combine these with the bounded runtime-binding automated proof before claiming live Tutor behavior impact. |
| Optional video | Human capture only | Deferred | No external video is required yet. |

Use these status values consistently:

- `Current`: still matches the latest successful smoke run.
- `Stale`: the MVP path changed after the last successful capture or validation.
- `Blocked`: refresh could not complete because smoke failed or the environment was unavailable.
- `Deferred`: intentionally skipped because the artifact is optional.

## Local Validation Summary

| Area | Command | Result |
| --- | --- | --- |
| Scripted demo reset | `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001` | Passed on 2026-04-26; it recreated `contest-demo-quadratics`, `contest-assessment-demo`, and `contest-tutor-demo` in the lane-6 worktree. |
| Backend health | `curl -s http://127.0.0.1:8001/api/v1/system/status` | Passed on 2026-04-26 with backend `online`, configured `gpt-4.1`, embeddings not configured, and fallback search provider `duckduckgo`. |
| Knowledge Pack presence | `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Passed on 2026-04-26; `contest-demo-quadratics` was present with demo-safe metadata and team-safe sharing status. |
| Dashboard overview | `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Passed on 2026-04-26 with recent activity including the contest assessment and tutor sessions grounded in `contest-demo-quadratics`. |
| Dashboard recent activity | `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Passed on 2026-04-26 with assessment and tutor activity grounded in `contest-demo-quadratics`. |
| Assessment evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Passed on 2026-04-26 and returned `context_support` plus demo-safe Knowledge Pack references. |
| Tutor evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Passed on 2026-04-26 and returned `context_support` plus demo-safe Knowledge Pack references. |
| Frontend production build | `cd web && npm ci && npm run build` | Passed on 2026-04-26 in lane 6, with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local` and the existing multiple-lockfile warning. |

## Current Known Limitations

- Video evidence is deferred unless the final contest submission requires it.
- The frontend build emits a Next.js warning about multiple lockfiles and inferred workspace root. The build still completes successfully.
- Browser-backed screenshot refresh now works in a local worktree, but it still depends on a running backend and frontend plus demo-safe local data.
- Runtime handoff from `config.agent_spec_id` through the unified live Tutor turn path now has bounded automated proof in repository tests, including a visible behavior difference between two spec packs. This report still does not claim universal wiring across every possible entry point.
- Diagnosis credibility is grounded in deterministic rules plus teacher review framing. This report does not claim benchmark accuracy numbers for diagnosis or recommendation quality.
- The repository currently documents no pilot cohort, classroom rollout, or real-user study. Use `PILOT_STATUS.md` for the explicit external-feedback status.
- Local provider-backed assessment generation was unavailable during the 2026-04-25 screenshot refresh because the configured model key was still a placeholder. The refreshed `07` and `08` screenshots therefore use demo-safe local session content in the worktree data store instead of a live provider response.
- Provider-backed AI quality depends on configured model credentials. If credentials are unavailable during a demo, use the command validation and recorded UI flow as fallback evidence.
- This report uses demo-safe descriptions only. Do not add real student data.

## Local Demo Run

The latest smoke-backed evidence refresh used local demo data only (2026-04-26):

- Reset: `python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`
- Backend: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m deeptutor_cli.main serve --host 127.0.0.1 --port 8001`
- Frontend validation: `npm ci && npm run build` in `web/` with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local`
- Knowledge Pack: `contest-demo-quadratics`
- Demo sessions:
  - `contest-assessment-demo`
  - `contest-tutor-demo`
- Screenshot refresh follow-up:
  - browser-backed recapture completed on 2026-04-26 for the dashboard evidence-first workflow and `/agents` authoring proof;
  - Knowledge Pack, assessment, and tutor screenshots remain valid from the 2026-04-25 refresh;
  - dashboard screenshots now point to the new evidence-first workflow captures;
  - hybrid `/agents` screenshot rows are current, and runtime-binding claims are now backed by bounded automated proof for the unified Tutor turn path rather than authoring-only wording.

Before future smoke or evidence refresh runs, use `DEMO_DATA_RESET.md` when local demo state may be missing or stale.

The local reset command is:

```bash
python3 -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001
```

The first backend attempt with `.venv/bin/python -m deeptutor.api.run_server` failed before binding because the reload configuration passed absolute `reload_excludes` paths to the installed `uvicorn`, which rejects non-relative glob patterns. The smoke run used the existing CLI server path with reload disabled instead.

The frontend build in this smoke pass completed successfully. It still emits the existing multiple-lockfile warning.

## Smoke-backed Verification Record

The 2026-04-26 scripted-reset smoke run verified the MVP path in the current merged state:

1. scripted reset recreated the demo-safe Knowledge Pack and assessment/tutor sessions in the fresh worktree;
2. backend started successfully with the repository-local virtual environment through the CLI server path;
3. system status, knowledge list, dashboard overview, dashboard recent, assessment session, and tutor session endpoints all returned the expected demo-safe data;
4. the frontend production build passed against `http://localhost:8001` after `npm ci` in the lane-6 worktree;
5. smoke-backed command evidence stayed `Current`, and browser-captured dashboard plus hybrid `/agents` rows were refreshed on 2026-04-26 against the current merged UI;
6. focused automated tests now prove the unified Tutor turn path can accept `config.agent_spec_id`, assemble the matching runtime policy, and produce a deterministic behavior difference between two contrasting spec packs without claiming full entry-point coverage.
7. diagnosis credibility is supported by focused rule-based cases in repository tests and a reviewer-facing case-study packet in `DIAGNOSIS_CASE_STUDIES.md`, not by fabricated accuracy metrics.

## Manual Verification Template

Complete this section when the local app is running.

| Step | Expected result | Status | Evidence link |
| --- | --- | --- | --- |
| Open Knowledge page | Teacher can create or edit Knowledge Pack metadata | Passed | [`01-knowledge-pack-metadata.png`](./screenshots/01-knowledge-pack-metadata.png) |
| Reload Knowledge page | Metadata remains visible | Passed | [`02-knowledge-pack-after-reload.png`](./screenshots/02-knowledge-pack-after-reload.png) |
| Open assessment config | Quiz generation mode shows the demo Knowledge Pack context | Passed | [`04-assessment-config.png`](./screenshots/04-assessment-config.png) |
| Generate assessment | Questions are generated from selected subject/context | Passed with demo-safe local session content | [`07-assessment-generated-questions.png`](./screenshots/07-assessment-generated-questions.png) |
| Review feedback | Common-mistake or guidance output is visible | Passed with demo-safe local session content | [`08-assessment-common-mistakes.png`](./screenshots/08-assessment-common-mistakes.png) |
| Ask Tutor Agent follow-up | Student prompt is visible before the tutor answer | Passed with seeded demo response | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Review tutor answer | Tutor responds to student question with learning context | Passed with seeded demo response | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Open Dashboard | Evidence-first teacher workflow is visible | Passed | [`05-dashboard-evidence-first-overview.png`](./screenshots/05-dashboard-evidence-first-overview.png) |
| Review dashboard recent activity | Assessment and tutoring activity still appears below the workflow | Passed | [`09-dashboard-recent-activity-evidence-first.png`](./screenshots/09-dashboard-recent-activity-evidence-first.png) |
| Open `/agents` authoring | Structured `IDENTITY`, `SOUL`, and `RULES` sections are visible | Passed | [`10-agents-spec-pack-authoring.png`](./screenshots/10-agents-spec-pack-authoring.png) |
| Show `/agents` export action | Export is visible from the authoring tab | Passed | [`11-agents-spec-pack-export.png`](./screenshots/11-agents-spec-pack-export.png) |

## PR Evidence Links

- Knowledge Pack MVP: PR `#6`.
- Assessment and Student Tutor Workspace MVP: PR `#8`.
- Teacher Dashboard MVP: PR `#11`.
- Contest evidence packet: PR `#13`.
- Screenshot capture refresh: PR `#15`.
- Demo-readiness smoke packet: PR `#23`.
- Demo-readiness smoke execution result: PR `#24`.
- Contest evidence refresh packet: PR `#27`.
- Scripted demo reset utility: PR `#36`.
- Contest smoke scripted reset packet: PR `#38`.

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

6. If the hybrid authoring UI changes again, recapture `/agents` authoring screenshots after a successful smoke cycle and update the freshness state accordingly.
