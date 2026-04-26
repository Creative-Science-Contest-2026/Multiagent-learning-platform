# Demo Script

Use this script to present the MVP in the same order as the project goal.

## Setup

1. Install backend and frontend dependencies according to the repository README.
2. Start the API server.
3. Start the web app.
4. Open the web workspace in a browser.
5. Use demo-safe sample content. Do not use private student data.

## Hybrid Presenter Check

Before the learning loop, optionally show a short teacher-authoring proof on `/agents`:

1. Open Agent Specs authoring.
2. Show structured sections (`IDENTITY`, `SOUL`, `RULES`) and free-form markdown sections.
3. Export the spec pack.

Do not claim that every live turn is already bound to a selected `agent_spec_id` unless that exact path is re-verified in the current smoke run.

## Demo Path

### 1. Teacher Creates A Knowledge Pack

Goal: show that a teacher can prepare class context before asking AI to generate learning activity.

Steps:

1. Open the Knowledge page.
2. Create or select a Knowledge Pack.
3. Fill the metadata fields:
   - subject;
   - grade;
   - curriculum;
   - learning objectives;
   - owner;
   - sharing status.
4. Save the pack.
5. Reload or revisit the page and confirm the metadata remains available.

Evidence to capture:

- Screenshot of the Knowledge page with demo-safe metadata.
- Screenshot after reload showing persisted metadata.

### 2. AI Generates An Assessment

Goal: show that the assessment workflow can use the teacher's subject and Knowledge Pack context.

Steps:

1. Open the assessment or quiz generation UI.
2. Select or reference the demo Knowledge Pack.
3. Set subject and quiz parameters.
4. Generate the assessment.
5. Review generated questions and common-mistake feedback.

Evidence to capture:

- Screenshot of the quiz configuration.
- Screenshot of generated questions.
- Screenshot of common-mistake guidance.

### 3. Student Learns With Tutor Agent

Goal: show that the student can continue learning with Tutor Agent context after assessment generation.

Steps:

1. Open the student tutoring/chat workspace.
2. Select the same Knowledge Pack when available.
3. Ask a student-style follow-up question.
4. Confirm the tutor response is grounded in the selected learning context.

Evidence to capture:

- Screenshot of the selected Knowledge Pack context.
- Screenshot of student question and Tutor Agent answer.

### 4. Teacher Reviews Dashboard

Goal: show that the teacher can review recent assessment and tutoring activity.

Steps:

1. Open the Dashboard page.
2. Confirm the teacher insight cards show `Observed`, `Inferred`, and `Recommended Action`.
3. Confirm small-group recommendation cards are visible when grouped signals exist.
4. Confirm recent activity still distinguishes assessment and tutoring sessions.
5. Confirm Knowledge Pack references appear when sessions used a selected pack.

Evidence to capture:

- Screenshot of the evidence-first teacher insight overview.
- Screenshot of recent activity with Knowledge Pack context below the insight workflow.

## Presenter Notes

- Keep the demo short and linear.
- Use one consistent sample topic across all screens.
- If an external LLM provider is unavailable, explain the unavailable credential and show the local validation report instead of inventing evidence.
- After the demo, open `VALIDATION_REPORT.md` to show exact commands and known limitations.
- If you include the hybrid authoring check, keep it under one minute and treat it as authoring proof unless runtime binding is re-verified in this environment.
