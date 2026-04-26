# Pitch Notes

## One-line pitch

An AI-first learning platform where Vietnamese teachers turn their own materials into classroom-ready tutoring, practice, and follow-up insight without giving up control over how the AI teaches.

## Problem

Teachers already have lesson materials and teaching instincts, but they do not have enough time to turn them into personalized practice, tutoring support, and follow-up decisions for each learner.

## Solution

The platform turns teacher-owned materials into Knowledge Packs, drafts assessments for teacher review, supports student tutoring, and gives teachers an evidence-first dashboard. Teachers can also set the tutor's class fit, support style, and guardrails on `/agents`, so the system adapts to how they want students to be helped, not just what content is covered.

Teacher-facing use cases:

1. A grade 6 teacher can make the tutor explain more gently, use simpler language, and avoid giving final answers too quickly.
2. A grade 10 teacher can make the tutor more Socratic, push for reasoning steps, and escalate when students keep repeating the same mistake.
3. A teacher reviewing the dashboard can spot which students need remediation now and which small group should revisit the same misconception together.

Dashboard actionability stories:

1. Repeated misses on one topic -> teacher move: reteach one prerequisite with one scaffolded example.
2. Fast but inconsistent answers -> teacher move: ask for one reasoning step before another hint.
3. Shared misconception cluster -> teacher move: pull one remediation mini-group before the next assessment.

## Why now

LLM agents, RAG, and AI-assisted content generation make it possible to reduce lesson preparation cost while keeping teachers in control of knowledge sources.

## MVP demo story

1. Teacher creates a Knowledge Pack.
2. Teacher generates questions from the pack.
3. Student studies with Tutor Agent grounded in the pack.
4. Teacher views dashboard evidence and teacher-reviewable diagnosis suggestions.

Behavior-diff story for judges:

- `IDENTITY` changes who the tutor is serving: subject, grade band, tone, and language.
- `SOUL` changes how the tutor reacts when a student is wrong, stuck, or discouraged.
- `RULES` changes the classroom boundaries: for example, whether the tutor should withhold direct answers, how much hinting is allowed, and when to stop or escalate.
- The same student question can therefore receive a more encouraging scaffolded response in one class setup and a more Socratic push-back in another, without changing the underlying source material.
