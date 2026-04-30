# Demo Script

Use this script to present the MVP in the same order as the project goal.

## Setup

1. Install backend and frontend dependencies according to the repository README.
2. Start the API server.
3. Start the web app.
4. Open the web workspace in a browser.
5. Use demo-safe sample content. Do not use private student data.

## Anchor Case Study

Keep the full presentation anchored to one classroom-safe story:

- Class: Grade 9 mathematics
- Knowledge Pack: `contest-demo-quadratics`
- Curriculum context: `Vietnam secondary algebra`
- Teacher goal: help students solve quadratic equations and explain common mistakes
- Student weakness pattern to narrate: factoring confusion plus missed root-checking
- Teacher decision point: use dashboard signals to choose one bounded remediation step or a small-group follow-up

If a presenter needs one sentence, use this:

> A Grade 9 math teacher prepares one quadratics Knowledge Pack, drafts one assessment from it, lets the student ask one grounded follow-up, then uses the dashboard to decide one bounded remediation move for the same misconception cluster.

## Presenter Metric Card

If a judge asks for a compact proof summary during the demo, use only these bounded metrics:

- `1` anchor Knowledge Pack: `contest-demo-quadratics`
- `2` verified demo sessions: `contest-assessment-demo` and `contest-tutor-demo`
- `2/2` verified sessions grounded in the same Knowledge Pack
- teacher-reviewed recommendation/intervention framing present in the dashboard and casepack docs

Do not expand this into diagnosis accuracy, learning gain, or classroom outcome claims.

## Hybrid Presenter Check

Before the learning loop, optionally show a short teacher-authoring proof on `/agents`:

1. Open Agent Specs authoring.
2. Explain the sections in teacher language:
   - `IDENTITY`: who this tutor is for;
   - `SOUL`: how it reacts when students are wrong or stuck;
   - `RULES`: what classroom boundaries it must respect.
3. Show one behavior-diff example:
   - a supportive class setup gives more encouragement and scaffolding;
   - an exam-prep setup pushes the student to justify steps before another hint.
4. Export the spec pack.

You may claim bounded proof that the unified Tutor turn path can bind `config.agent_spec_id` and change runtime behavior between two contrasting spec packs. Do not expand that into a claim about every entry point unless the broader path is re-verified in the current smoke run.

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
5. Show that the generated assessment is treated as a draft requiring teacher review.
6. Review generated questions and common-mistake feedback.
7. Explain that a teacher can approve, edit, or reject before student-facing reuse.

Presenter framing for the anchor case:

- the assessment is still about quadratic equations from the same pack
- the weakness pattern to watch for is factoring and root-checking, not a random generic topic

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

Anchor follow-up prompt example:

- ask the tutor to help a student understand a common factoring mistake and why both roots still need to be checked against the original equation

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
6. Explain one concrete teacher move for the same quadratics case: the teacher sees repeated factoring confusion and decides to reteach one prerequisite plus pull a remediation mini-group before the next check.
7. Keep the dashboard explanation inside one bounded story:
   - observed: repeated difficulty on one quadratics sub-skill
   - inferred: likely misconception cluster worth teacher review
   - teacher move: one scaffolded reteach or one mini-group follow-up

Evidence to capture:

- Screenshot of the structured `/agents` authoring tab.
- Screenshot of the visible export action for the saved spec pack.
- Screenshot of the evidence-first teacher insight overview.
- Screenshot of recent activity with Knowledge Pack context below the insight workflow.

## Presenter Notes

- Keep the demo short and linear.
- Use one consistent sample topic across all screens.
- Prefer the same quadratics story on every screen instead of switching examples mid-demo.
- When explaining `/agents`, start with classroom outcomes before architecture words.
- If an external LLM provider is unavailable, explain the unavailable credential and show the local validation report instead of inventing evidence.
- After the demo, open `VALIDATION_REPORT.md` to show exact commands and known limitations.
- If you include the hybrid authoring check, keep it under one minute. The safe claim is: authoring is visible in UI, and the current repository also contains bounded automated proof that the unified Tutor turn path changes behavior across two contrasting spec packs.
- For assessment safety, the safe claim is: teacher review is the primary quality gate, not hidden model infallibility.
