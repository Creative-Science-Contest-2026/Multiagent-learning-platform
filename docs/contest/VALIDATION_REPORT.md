# Validation Report

Last updated: 2026-04-28

## Scope

This report covers the current contest MVP path:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

This report validates prototype behavior and contest evidence only. It is not a classroom outcome study or deployment report.

## Anchor Case And Bounded Metrics

Primary docs story for this report:

- Knowledge Pack: `contest-demo-quadratics`
- Class level: `Grade 9`
- Curriculum: `Vietnam secondary algebra`
- Learning objective: solve quadratic equations and explain common mistakes
- Weakness pattern used in the demo story: factoring confusion and missed root-checking
- Teacher decision surface: dashboard-reviewed remediation, not autonomous intervention

Bounded metric card for the current evidence set:

| Metric | Current value | Evidence basis |
| --- | --- | --- |
| Demo-safe Knowledge Packs in the anchor story | `1` | `contest-demo-quadratics` from the reset inventory and knowledge-list validation |
| Verified demo sessions tied to that pack | `2` | `contest-assessment-demo` and `contest-tutor-demo` from local validation |
| Verified command-backed loop checkpoints | `4` | Knowledge Pack presence, assessment session, tutor session, and dashboard review endpoints |
| Knowledge Pack grounding coverage in verified sessions | `2/2` | both validated sessions reference `contest-demo-quadratics` |
| Teacher recommendation/intervention framing present | `Yes` | dashboard review flow, diagnosis case studies, and casepack framing |

Explicit non-claims:

- no diagnosis accuracy benchmark
- no classroom outcome metric
- no learning-gain claim
- no pilot effectiveness claim

## Evidence Freshness Status

Latest smoke-backed refresh: 2026-04-28

Structured command-backed status artifact: `../../ai_first/evidence/evidence_status.json`

| Evidence group | Refresh mode | Status | Latest source |
| --- | --- | --- | --- |
| Backend and API reachability | Auto after smoke | Current | Scripted-reset smoke run repeated on 2026-04-28 and recorded in `ai_first/daily/2026-04-28.md`. |
| Frontend production build | Auto after smoke | Current | `npm ci && npm run build` passed on 2026-04-28 with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local` in the Session B worktree. |
| Screenshot bundle | Browser capture after smoke when the UI changes | Stale | Last real browser recapture remains 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; after Phase 2 polish merged in PRs `#214`, `#215`, and `#216`, the browser screenshots no longer fully match the current UI. |
| Hybrid authoring screenshots (`/agents`) | Browser capture after smoke when hybrid story is presented | Stale | Last real browser recapture remains 2026-04-26 in `docs/evidence-dashboard-agents-recapture`; `/agents` wording changed in PR `#215`, so recapture is required before claiming these screenshots match current UI. |
| Optional video | Human capture only | Deferred | No external video is required yet. |

Use these status values consistently:

- `Current`: still matches the latest successful smoke run.
- `Stale`: the MVP path changed after the last successful capture or validation.
- `Blocked`: refresh could not complete because smoke failed or the environment was unavailable.
- `Deferred`: intentionally skipped because the artifact is optional.

## Local Validation Summary

| Area | Command | Result |
| --- | --- | --- |
| Scripted demo reset | `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001` | Passed on 2026-04-28; it recreated `contest-demo-quadratics`, `contest-assessment-demo`, and `contest-tutor-demo` in the Session B worktree. |
| Backend health | `curl -s http://127.0.0.1:8001/api/v1/system/status` | Passed on 2026-04-28 with backend `online`, configured `gpt-4o-mini`, embeddings not configured, and fallback search provider `duckduckgo`. |
| Knowledge Pack presence | `curl -s http://127.0.0.1:8001/api/v1/knowledge/list` | Passed on 2026-04-28; `contest-demo-quadratics` was present with demo-safe metadata and `sharing_status: demo`. |
| Dashboard overview | `curl -s http://127.0.0.1:8001/api/v1/dashboard/overview` | Passed on 2026-04-28 with recent activity including the contest assessment and tutor sessions grounded in `contest-demo-quadratics`. |
| Dashboard recent activity | `curl -s http://127.0.0.1:8001/api/v1/dashboard/recent` | Passed on 2026-04-28 with assessment and tutor activity grounded in `contest-demo-quadratics`. |
| Assessment evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-assessment-demo` | Passed on 2026-04-28 and returned `context_support` plus demo-safe Knowledge Pack references. |
| Tutor evidence session | `curl -s http://127.0.0.1:8001/api/v1/sessions/contest-tutor-demo` | Passed on 2026-04-28 and returned `context_support` plus demo-safe Knowledge Pack references. |
| Frontend production build | `cd web && npm ci && npm run build` | Passed on 2026-04-28 in Session B, with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local` and the existing multiple-lockfile warning. |

## Current Known Limitations

- Video evidence is deferred unless the final contest submission requires it.
- The frontend build emits a Next.js warning about multiple lockfiles and inferred workspace root. The build still completes successfully.
- Browser-backed screenshot refresh now works in a local worktree, but it still depends on a running backend and frontend plus demo-safe local data.
- Runtime handoff from `config.agent_spec_id` through the unified live Tutor turn path now has bounded automated proof in repository tests, including a visible behavior difference between two spec packs. This report still does not claim universal wiring across every possible entry point.
- Diagnosis credibility is grounded in deterministic rules plus teacher review framing. This report does not claim benchmark accuracy numbers for diagnosis or recommendation quality.
- Structured validation scenarios now live in `ai_first/evidence/casepack.json` and are explained in `CASEPACK_AND_EVALUATION_DATASET.md`; they support repeatable review without becoming a benchmark claim.
- Command-backed evidence refresh can now be summarized through `ai_first/evidence/evidence_status.json`; this improves repeatability but does not automate screenshot or video capture.
- The repository currently documents no pilot cohort, classroom rollout, or real-user study. Use `PILOT_STATUS.md` for the explicit external-feedback status.
- Local provider-backed assessment generation was unavailable during the 2026-04-25 screenshot refresh because the configured model key was still a placeholder. The refreshed `07` and `08` screenshots therefore use demo-safe local session content in the worktree data store instead of a live provider response.
- Provider-backed AI quality depends on configured model credentials. If credentials are unavailable during a demo, use the command validation and recorded UI flow as fallback evidence.
- The 2026-04-28 smoke pass verified seeded demo-safe assessment and tutor sessions plus Knowledge Pack grounding through API responses. It did not freshly recapture browser evidence for diagnosis or intervention surfaces.
- After Phase 2 polish merged in PRs `#214`, `#215`, and `#216`, the Knowledge, Tutor, Dashboard, and `/agents` screenshots should be treated as stale until a fresh browser recapture is completed.
- This report uses demo-safe descriptions only. Do not add real student data.

## Local Demo Run

The latest smoke-backed evidence refresh used local demo data only (2026-04-28):

- Reset: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001`
- Backend: `/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m deeptutor_cli.main serve --host 127.0.0.1 --port 8001`
- Frontend validation: `npm ci && npm run build` in `web/` with `NEXT_PUBLIC_API_BASE=http://localhost:8001` from `web/.env.local`
- Knowledge Pack: `contest-demo-quadratics`
- Demo sessions:
  - `contest-assessment-demo`
  - `contest-tutor-demo`
- Screenshot refresh follow-up:
  - Session B did not perform a fresh browser recapture on 2026-04-28;
  - assessment screenshots still match the latest merged assessment UI and remain current from the 2026-04-25 browser refresh;
  - Knowledge Pack, Tutor, Dashboard, and `/agents` screenshots are now stale because later Phase 2 polish changed visible UI/copy after those captures;
  - hybrid `/agents` screenshot rows still require the bounded runtime-binding automated proof when discussing live Tutor behavior impact.

Before future smoke or evidence refresh runs, use `DEMO_DATA_RESET.md` when local demo state may be missing or stale.

The local reset command is:

```bash
/Users/nguyenhuuloc/Documents/Multiagent-learning-platform/.venv/bin/python -m scripts.contest.reset_demo_data --project-root . --api-base http://localhost:8001
```

The first backend attempt with `.venv/bin/python -m deeptutor.api.run_server` failed before binding because the reload configuration passed absolute `reload_excludes` paths to the installed `uvicorn`, which rejects non-relative glob patterns. The smoke run used the existing CLI server path with reload disabled instead.

The frontend build in this smoke pass completed successfully. It still emits the existing multiple-lockfile warning.

## Smoke-backed Verification Record

The 2026-04-28 scripted-reset smoke run verified the MVP path in the current merged state:

1. scripted reset recreated the demo-safe Knowledge Pack and assessment/tutor sessions in the fresh worktree;
2. backend started successfully with the repository-local virtual environment through the CLI server path;
3. system status, knowledge list, dashboard overview, dashboard recent, assessment session, and tutor session endpoints all returned the expected demo-safe data;
4. the frontend production build passed against `http://localhost:8001` after `npm ci` in the Session B worktree;
5. smoke-backed command evidence is current on 2026-04-28, while browser-captured Knowledge, Tutor, Dashboard, and `/agents` rows are now stale after later Phase 2 polish merges;
6. this smoke pass proves the command-backed Knowledge Pack -> Assessment session -> Tutor session -> Dashboard path with demo-safe seeded content and retained Knowledge Pack grounding, but it does not newly prove the latest polished browser UI;
7. focused automated tests still provide the bounded proof that the unified Tutor turn path can accept `config.agent_spec_id`, assemble the matching runtime policy, and produce a deterministic behavior difference between two contrasting spec packs without claiming full entry-point coverage;
8. diagnosis credibility remains supported by focused rule-based cases and the reviewer-facing case-study packet in `DIAGNOSIS_CASE_STUDIES.md`, not by fabricated accuracy metrics or a fresh Session B browser run;
9. reusable validation examples remain available as a machine-readable casepack in `ai_first/evidence/casepack.json`, intended for future regression and evidence-automation work rather than runtime scoring.

## Manual Verification Template

Complete this section when the local app is running.

| Step | Expected result | Status | Evidence link |
| --- | --- | --- | --- |
| Open Knowledge page | Teacher can create or edit Knowledge Pack metadata | Stale after PR `#214` | [`01-knowledge-pack-metadata.png`](./screenshots/01-knowledge-pack-metadata.png) |
| Reload Knowledge page | Metadata remains visible | Stale after PR `#214` | [`02-knowledge-pack-after-reload.png`](./screenshots/02-knowledge-pack-after-reload.png) |
| Open assessment config | Quiz generation mode shows the demo Knowledge Pack context | Passed | [`04-assessment-config.png`](./screenshots/04-assessment-config.png) |
| Generate assessment | Questions are generated from selected subject/context | Passed with demo-safe local session content | [`07-assessment-generated-questions.png`](./screenshots/07-assessment-generated-questions.png) |
| Review feedback | Common-mistake or guidance output is visible | Passed with demo-safe local session content | [`08-assessment-common-mistakes.png`](./screenshots/08-assessment-common-mistakes.png) |
| Ask Tutor Agent follow-up | Student prompt is visible before the tutor answer | Stale after PRs `#214` and `#215` | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Review tutor answer | Tutor responds to student question with learning context | Stale after PRs `#214` and `#215` | [`06-tutor-agent-answer.png`](./screenshots/06-tutor-agent-answer.png) |
| Open Dashboard | Evidence-first teacher workflow is visible | Stale after PRs `#214` and `#215` | [`05-dashboard-evidence-first-overview.png`](./screenshots/05-dashboard-evidence-first-overview.png) |
| Review dashboard recent activity | Assessment and tutoring activity still appears below the workflow | Stale after PRs `#214` and `#215` | [`09-dashboard-recent-activity-evidence-first.png`](./screenshots/09-dashboard-recent-activity-evidence-first.png) |
| Open `/agents` authoring | Structured `IDENTITY`, `SOUL`, and `RULES` sections are visible | Stale after PR `#215` | [`10-agents-spec-pack-authoring.png`](./screenshots/10-agents-spec-pack-authoring.png) |
| Show `/agents` export action | Export is visible from the authoring tab | Stale after PR `#215` | [`11-agents-spec-pack-export.png`](./screenshots/11-agents-spec-pack-export.png) |

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

6. Recapture Knowledge, Tutor, Dashboard, and `/agents` screenshots against the current merged Phase 2 polish state before returning those rows to `Current`.
