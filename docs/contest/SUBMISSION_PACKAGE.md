# Contest Submission Package

Use this as the short review path before submitting the VnExpress Sang kien Khoa hoc 2026 MVP.

## Submission Story

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

One-line pitch:

An AI-first learning platform where Vietnamese teachers create Knowledge Packs and teaching skills, then AI Tutor Agents help students learn, practice, and improve from teacher-approved materials.

Primary pitch source: [`ai_first/competition/pitch-notes.md`](../../ai_first/competition/pitch-notes.md).

## Ready Evidence

| Item | Status | Source |
| --- | --- | --- |
| Demo script | Ready | [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md) |
| Smoke-backed validation | Ready | [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md) |
| Evidence checklist | Ready | [`EVIDENCE_CHECKLIST.md`](./EVIDENCE_CHECKLIST.md) |
| Screenshot bundle | Ready | [`screenshots/`](./screenshots/) |
| Demo-safe reset command | Ready | [`DEMO_DATA_RESET.md`](./DEMO_DATA_RESET.md) |
| Smoke procedure | Ready | [`SMOKE_RUNBOOK.md`](./SMOKE_RUNBOOK.md) |
| Contest rules summary | Ready | [`ai_first/competition/vnexpress-rules-summary.md`](../../ai_first/competition/vnexpress-rules-summary.md) |
| Final checklist | In review | [`ai_first/competition/submission-checklist.md`](../../ai_first/competition/submission-checklist.md) |
| Optional video | Deferred | Record only if final submission requires a video artifact. |

## Latest Validation

The latest smoke-backed refresh passed on 2026-04-19 after running the scripted local reset. It verified:

- demo-safe Knowledge Pack `contest-demo-quadratics`;
- assessment session `contest-assessment-demo`;
- tutor session `contest-tutor-demo`;
- dashboard overview and recent activity;
- frontend production build with `NEXT_PUBLIC_API_BASE=http://localhost:8001`.

Detailed command evidence lives in [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md). The execution PR is `#40`.

## Human Review Checklist

Before final submission, a human should review:

- product description and category fit for the Education field;
- intellectual property commitment;
- whether optional video is required;
- screenshots for clarity and absence of private data;
- known limitations and environment notes in [`VALIDATION_REPORT.md`](./VALIDATION_REPORT.md);
- Apache 2.0 license and HKUDS/DeepTutor attribution.

## Known Limitations

- Optional video is deferred to avoid storing large media in the repository.
- Provider-backed AI quality depends on configured model credentials.
- The backend `deeptutor.api.run_server` path has a reload/absolute-pattern incompatibility with the installed `uvicorn`; latest smoke used the CLI server path with reload disabled.
- Frontend build may need network access to fetch Google Fonts.
- Screenshots should be recaptured only if the UI meaningfully changes.

## Review Flow

```mermaid
flowchart TD
  Package["SUBMISSION_PACKAGE.md"]
  Pitch["Pitch notes"]
  Demo["Demo script"]
  Evidence["Evidence checklist"]
  Validation["Validation report"]
  Screenshots["Screenshots"]
  Human["Human final review"]

  Package --> Pitch
  Package --> Demo
  Package --> Evidence
  Package --> Validation
  Evidence --> Screenshots
  Validation --> Human
  Screenshots --> Human
```
