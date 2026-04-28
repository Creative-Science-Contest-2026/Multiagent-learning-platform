# Fork Modifications Note

## Upstream Base

This repository is a contest-focused fork of `HKUDS/DeepTutor`, which remains credited in `README.md` and `AGENTS.md` and stays under the Apache 2.0 license retained in `LICENSE`.

## Purpose of This Fork

The fork narrows the broad DeepTutor platform into a stable VnExpress Sáng kiến Khoa học 2026 MVP for the Education field. The submission story is:

Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention.

The dashboard remains the teacher-facing operating surface for reviewing diagnosis and choosing interventions, but it should not replace the five-step contest loop as the official product scope.

## Major Modifications Added in This Fork

### 1. Teacher-owned Knowledge Pack workflow

- teacher metadata and sharing controls for packs
- teacher invitation metadata for collaboration
- knowledge-pack version metadata for safer reuse and tracking

### 2. Marketplace workflow for reusable packs

- real marketplace import instead of placeholder behavior
- pack preview, ratings, sorting, cache optimization, and full-text search
- batch import and offline-ready imported-pack fallback
- mobile-first marketplace layout

### 3. Assessment workflow improvements

- richer assessment review insights and recommendations
- adaptive difficulty selection
- assessment export to PDF
- assessment timing metrics and review visibility in the dashboard

### 4. Tutor Agent workflow improvements

- KB context badges during tutoring
- tutor follow-up prompts
- tutoring session replay for teacher review

### 5. Teacher and student dashboard views

- teacher analytics and activity views
- student progress dashboard and learning-path sequencing
- filtering and recent-session visibility for review workflows
- teacher-reviewable diagnosis and intervention follow-up context

### 6. Contest-readiness and operating layer

- Vietnamese MVP prompt coverage
- route error boundaries and API rate limiting for safer demo behavior
- offline quiz-result sync queue for unreliable-network scenarios
- contest smoke, screenshot, and submission evidence bundle under `docs/contest/`
- AI-first operating control-plane files under `ai_first/` for autonomous task execution

## Key Repository Areas Showing These Changes

- `deeptutor/api/routers/`
- `deeptutor/agents/`
- `deeptutor/services/`
- `web/app/`
- `web/components/`
- `web/lib/`
- `docs/contest/`
- `ai_first/`

## Submission Use

This note exists to satisfy the submission-checklist item `Fork modifications described` with a concise, repo-backed explanation of how this fork differs from upstream HKUDS/DeepTutor for the contest MVP.

Scope guardrail for submission wording:

- position the fork as a teacher-controlled adaptive tutoring prototype
- treat marketplace, export, replay, and offline helpers as supporting proof
- do not present the current repository as a full classroom deployment or autonomous multi-agent system
