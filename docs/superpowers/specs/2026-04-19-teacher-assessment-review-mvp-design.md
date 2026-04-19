# Teacher Assessment Review MVP Design

## Summary

Add a teacher-facing assessment review flow that starts from the existing Dashboard and drills down into a dedicated review page for one assessment session.

This closes the current contest MVP gap between "AI generated an assessment" and "teacher can see what the student actually got right or wrong." The result should support the full story:

Teacher creates Knowledge Pack -> AI generates assessment -> Student answers assessment -> Teacher reviews assessment results.

## Problem

The current product stores quiz results, but the teacher-facing product surface only exposes session-level activity. Teachers can see that an assessment session happened, but they cannot review score, correct versus incorrect answers, or the session's assessment details in a structured way.

That weakens the contest story because the product demonstrates generation and tutoring, but not clear instructional feedback after assessment completion.

## Goals

- Keep the current Dashboard as a summary surface.
- Add a drill-down review page for a single assessment session.
- Show score, correct count, incorrect count, and question-level review data.
- Preserve the existing Knowledge Pack linkage so teachers can understand which pack informed the assessment.
- Reuse the current session storage model as much as possible for MVP speed and low risk.

## Non-Goals

- Do not add assignment, class roster, or multi-student management.
- Do not redesign the whole Dashboard information architecture.
- Do not add a new analytics warehouse or reporting subsystem.
- Do not require live provider calls to review past assessment results.
- Do not broaden this into a general-purpose session transcript viewer for every capability.

## User Flow

### Dashboard Summary

The teacher opens Dashboard and sees:

- overall session totals as today;
- recent activity including assessment sessions;
- assessment-specific summary information surfaced more clearly for assessment rows, such as score or answered-question count when available.

From a recent assessment row, the teacher can open a dedicated review page.

### Assessment Review Page

The teacher opens one assessment session review page and sees:

- assessment title or session name;
- timestamp and session status;
- linked Knowledge Pack names;
- score percentage;
- count of correct and incorrect answers;
- per-question review cards with question text, learner answer, correct answer, and correctness state.

The page should be understandable without reading raw session transcript text.

## Product Requirements

### 1. Structured Assessment Review Contract

The backend must expose an assessment-review response object for one session. At minimum it should include:

- session id;
- title;
- timestamp;
- status;
- Knowledge Pack names;
- total questions;
- correct count;
- incorrect count;
- score percentage;
- ordered question results.

Each question result should include:

- question id when available;
- question text;
- learner answer;
- correct answer;
- correctness boolean.

### 2. Dashboard Drill-down Link

Recent assessment activity on Dashboard must link to the dedicated assessment review page.

The Dashboard stays summary-first. It should not inline the entire review experience.

### 3. Dedicated Review Route

Add a new teacher-facing route under the existing workspace/dashboard area for a single assessment session review.

The route should load directly from session id so it is shareable within the local product context and easy to link from Dashboard.

### 4. Knowledge Pack Context

If the reviewed assessment session used one or more Knowledge Packs, show those names in both summary and detail views when present.

### 5. Empty/Error States

If a session exists but does not have structured assessment result data, the review page should show a clear fallback state instead of crashing.

If the session id is missing or not found, show a clean not-found or request-failed state.

## Data Strategy

For MVP, do not introduce a new database table unless current session data proves insufficient.

Preferred approach:

1. Reuse the existing session store.
2. Extract assessment result structure from the quiz-result data already recorded for assessment sessions.
3. Centralize extraction logic in a helper close to session/dashboard APIs so both the overview and drill-down endpoints use the same parser.

If the current stored representation is too lossy, add the smallest compatible enrichment needed at the session-writing layer so future assessments retain structured result data without breaking old sessions.

## Technical Design

### Backend

Add backend support in the dashboard/session surface for:

- deriving structured assessment review data from one session;
- exposing a dedicated endpoint for one assessment review;
- optionally enriching dashboard overview rows for assessment sessions with review summary fields when available.

The extraction logic should not live inline in the route handler. Put it in a focused helper so tests can cover old and new session shapes independently.

### Frontend

Update Dashboard to:

- recognize assessment rows as drill-down targets;
- show a clear affordance to open review details;
- optionally surface a compact score badge or answered count if available.

Add a dedicated assessment review page that renders:

- metadata header;
- summary metric cards;
- ordered question review list.

Keep the page visually aligned with the current workspace/dashboard language rather than inventing a new design system.

## Backward Compatibility

- Existing sessions without structured quiz review data must not break the Dashboard.
- Review endpoints should degrade gracefully for old sessions.
- Existing tutoring and non-assessment session behavior must remain unchanged.

## Testing

### Backend

Add coverage for:

- dashboard overview with assessment summary data;
- dedicated review endpoint for a valid assessment session;
- graceful fallback when session exists without review payload;
- not-found behavior for missing session id.

### Frontend

Validate:

- Dashboard renders review links for assessment rows;
- review page loads session review data and renders summary plus question list;
- loading, empty, and error states are readable.

### Regression

Keep current dashboard and session persistence tests green.

## Task Decomposition Recommendation

Split execution into three packets:

1. Docs packet:
   create the feature task packet and shared handoff contract.
2. Backend/shared-contract packet:
   session review extraction, dashboard API enrichment, dedicated review endpoint, backend tests.
3. Frontend packet:
   dashboard drill-down UI, new review page, frontend API client updates, manual verification notes.

This split reduces conflict risk for multiple AI workers because backend and frontend ownership stay mostly separate.

## Risks

- Current quiz results may be stored in a text-heavy shape that is harder to parse reliably for legacy sessions.
- Dashboard and review page can drift if they compute assessment summaries differently.
- Too much dashboard detail would blur the separation between summary and drill-down.

## Mitigations

- Use one shared backend extraction path for both summary and detail.
- Keep Dashboard compact and push detail into the review page.
- Treat legacy sessions as partial-review capable rather than forcing perfect reconstruction.

## Acceptance Snapshot

The feature is successful when:

- a teacher can see that an assessment occurred from Dashboard;
- the teacher can open a dedicated review page for that assessment session;
- the review page shows score and per-question correctness in a structured way;
- the session still shows Knowledge Pack context when applicable;
- the feature remains compatible with the current contest MVP flow and AI-first execution model.
