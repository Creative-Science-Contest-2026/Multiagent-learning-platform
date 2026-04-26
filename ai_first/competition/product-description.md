# Contest Product Description Draft

## Product Name

Multiagent Learning Platform

## Field

Education

## Short Description

Multiagent Learning Platform is an AI-first learning platform that helps Vietnamese teachers turn their own teaching materials into reusable Knowledge Packs, draft assessments, support student tutoring, and review learning progress through one connected workflow while still deciding how the AI should teach.

## Problem

Teachers often already have lesson materials, exercises, and teaching experience, but they do not have enough time to convert those resources into personalized practice, tutoring support, and progress tracking for each learner. Many AI tools also generate content without grounding it in teacher-approved materials, which makes classroom adoption harder.

## Solution

The platform keeps teachers in control of the source knowledge. A teacher creates or imports a Knowledge Pack, uses AI to generate an assessment, lets students learn with a Tutor Agent grounded in that same pack, and then reviews the resulting activity in a teacher dashboard. This creates one practical loop:

Teacher creates Knowledge Pack -> AI generates assessment -> Student learns with Tutor Agent -> Teacher sees dashboard.

Within that loop, diagnosis and recommendation outputs are positioned as evidence-backed, confidence-tagged, teacher-reviewed hypotheses rather than autonomous final judgments. The `/agents` flow adds one more teacher-control layer: the teacher can decide who the tutor is for, how it should respond when students are wrong or stuck, and which classroom guardrails it must respect.

## Concrete Teacher Use Cases

1. A lower-secondary math teacher can set a calmer tone, simpler language, and stronger hint scaffolding for students who lose confidence quickly.
2. An exam-prep teacher can set a more demanding style that asks students to justify each step before the tutor gives another hint.
3. After class, a teacher can review the dashboard to see which students need individual follow-up and which small group should revisit the same misconception together.

## Main Capabilities in the Current MVP

1. Knowledge Pack management for teacher-owned learning materials and metadata.
2. Marketplace import and batch import for reusable packs.
3. AI-generated assessments with review insights, timing metrics, and export support.
4. Tutor Agent sessions with context badges, follow-up prompts, and replay support.
5. Teacher dashboard analytics for recent activity, student-facing learning progress, and teacher-reviewable diagnosis/recommendation signals.
6. Contest-ready evidence bundle with smoke-backed validation, screenshots, and demo-safe reset workflow.

## Why It Is Useful in Vietnam

- It supports a realistic classroom workflow where teachers remain responsible for the learning source.
- It reduces preparation time for quizzes, tutoring support, and follow-up review.
- It fits Vietnamese school usage through localized prompt variants and a demo story built around secondary algebra.
- It can help schools with limited content-production capacity reuse teacher knowledge more effectively.

## Innovation

The platform combines agent workflows, retrieval grounded in teacher-approved materials, assessment generation, tutoring, and dashboard review into one connected product path instead of isolated tools. Its practical novelty is not only “using AI,” but using AI while preserving teacher control over source content, teaching style, and evidence review.

## Practical Applicability

The current MVP already demonstrates the end-to-end classroom loop locally with demo-safe data and repeatable smoke validation. That makes it suitable for contest review, pilot demonstrations, and iterative deployment in education settings where reliability and explainability matter.

## Efficiency Impact

- Reduces manual work needed to turn teaching materials into assessments.
- Gives students immediate tutoring support based on the same approved knowledge source.
- Gives teachers a faster feedback loop through dashboard activity, assessment review, and next-step intervention suggestions.

## Development Potential

The current repository already includes the core product loop plus surrounding capabilities such as marketplace reuse, analytics, session replay, offline-ready imported packs, and submission-ready evidence. This gives the project a practical base for further school pilots, subject expansion, and commercialization research after the contest.

## Current Submission Status

This file is a draft intended to satisfy the “product description drafted” step in the submission checklist. It still requires final human review for wording, claim calibration, and submission-form formatting.
