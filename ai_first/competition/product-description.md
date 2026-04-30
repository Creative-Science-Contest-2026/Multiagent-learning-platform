# Contest Product Description Draft

## Product Name

Multiagent Learning Platform

## Field

Education

## Short Description

Multiagent Learning Platform is a teacher-controlled adaptive tutoring platform that helps Vietnamese teachers turn their own teaching materials into reusable Knowledge Packs, draft assessments, support student tutoring, review AI-assisted diagnosis, and decide the next intervention while still controlling how the AI should teach.

Current proof level: a validated prototype with contest-safe walkthrough validation, smoke-backed checks, and refreshed UI evidence.

## Problem

Teachers often already have lesson materials, exercises, and teaching experience, but they do not have enough time to convert those resources into personalized practice, tutoring support, and progress tracking for each learner. Many AI tools also generate content without grounding it in teacher-approved materials, which makes classroom adoption harder.

## Solution

The platform keeps teachers in control of the source knowledge. A teacher creates or imports a Knowledge Pack, uses AI to generate an assessment, lets students learn with a Tutor Agent grounded in that same pack, reviews teacher-facing diagnosis signals, and then decides the next intervention. This creates one practical loop:

Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention.

The teacher dashboard remains the operating surface that helps the teacher inspect that loop, but the product claim should stay anchored to the five-step learning cycle above rather than a generic reporting story.

Within that loop, diagnosis and recommendation outputs are positioned as evidence-backed, confidence-tagged, teacher-reviewed hypotheses rather than autonomous final judgments. The `/agents` flow adds one more teacher-control layer: the teacher can decide who the tutor is for, how it should respond when students are wrong or stuck, and which classroom guardrails it must respect.

Contest-safe case study anchor: a Grade 9 math teacher prepares `contest-demo-quadratics`, notices a learner repeatedly mixing up sign reasoning and factor pairs, uses the tutor for grounded scaffolded follow-up, and then reviews the dashboard to choose whether one student or a small group needs prerequisite reteaching next.

## Concrete Teacher Use Cases

1. A lower-secondary math teacher can set a calmer tone, simpler language, and stronger hint scaffolding for students who lose confidence quickly.
2. An exam-prep teacher can set a more demanding style that asks students to justify each step before the tutor gives another hint.
3. After class, a teacher can review the dashboard to see which students need individual follow-up and which small group should revisit the same misconception together.

## Main Capabilities in the Current MVP

1. Knowledge Pack management for teacher-owned learning materials and metadata.
2. Marketplace import and batch import for reusable packs.
3. AI-generated assessments with review insights, timing metrics, and export support.
4. Tutor Agent sessions with context badges, follow-up prompts, and replay support.
5. Teacher-reviewable diagnosis and intervention workflow surfaced through dashboard analytics, recent activity, and teacher-facing learning signals.
6. Contest-ready evidence bundle with smoke-backed validation, screenshots, and demo-safe reset workflow.

## Submission Scope Freeze

In-scope contest story:

- teacher-controlled adaptive tutoring for Vietnamese classrooms
- the five-step learning loop: `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`
- teacher-owned control over tutor identity, teaching style, and guardrails through `/agents`
- validated-prototype proof through smoke-backed walkthroughs, screenshots, and contest docs

Secondary but not core proof:

- marketplace reuse and batch import
- assessment export, replay, and timing support
- offline-ready fallback and sync-resilience helpers

Out of current claim scope:

- classroom outcome evidence
- school-scale deployment
- fully autonomous multi-agent operation without teacher review
- universal runtime proof across every capability and entry point

## Why It Is Useful in Vietnam

- It supports a realistic classroom workflow where teachers remain responsible for the learning source.
- It reduces preparation time for quizzes, tutoring support, and follow-up review.
- It fits Vietnamese school usage through localized prompt variants and a demo story built around secondary algebra.
- It can help schools with limited content-production capacity reuse teacher knowledge more effectively.

## Innovation

The platform combines agent workflows, retrieval grounded in teacher-approved materials, assessment generation, tutoring, diagnosis support, and intervention decision support into one connected product path instead of isolated tools. Its practical novelty is not only “using AI,” but using AI while preserving teacher control over source content, teaching style, and evidence review.

Its future direction can be described as multi-agent by design, because the architecture is prepared for stronger role separation later. The current merged product should still be described as an agent-native validated prototype rather than a full autonomous multi-agent deployment.

## Practical Applicability

The current MVP already demonstrates the end-to-end classroom loop locally with demo-safe data and repeatable smoke validation. That makes it suitable for contest review, pilot demonstrations, and iterative deployment in education settings where reliability and explainability matter.

This repository does not currently claim classroom outcome evidence or a scaled real-user pilot.

## Efficiency Impact

- Reduces manual work needed to turn teaching materials into assessments.
- Gives students immediate tutoring support based on the same approved knowledge source.
- Gives teachers a faster feedback loop through dashboard activity, assessment review, and next-step intervention suggestions.
- The current bounded proof is operational: one demo-safe Knowledge Pack, two verified demo-safe sessions, and one teacher-review loop. It is not classroom outcome proof.

## Development Potential

The current repository already includes the core product loop plus surrounding capabilities such as marketplace reuse, analytics, session replay, offline-ready imported packs, and submission-ready evidence. This gives the project a practical base for further school pilots, subject expansion, and commercialization research after the contest.

## Current Submission Status

This file is a draft intended to satisfy the “product description drafted” step in the submission checklist. It still requires final human review for wording, claim calibration, and submission-form formatting.
