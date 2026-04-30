# Pitch Notes

## One-line pitch

A teacher-controlled adaptive tutoring platform where Vietnamese teachers turn their own materials into classroom-ready practice, tutoring, diagnosis review, and follow-up intervention without giving up control over how the AI teaches.

Current status: validated prototype with smoke-backed demo evidence, not a deployed classroom system.

## Problem

Teachers already have lesson materials and teaching instincts, but they do not have enough time to turn them into personalized practice, tutoring support, and follow-up decisions for each learner.

## Solution

The platform turns teacher-owned materials into Knowledge Packs, drafts assessments for teacher review, supports student tutoring, surfaces diagnosis signals for teacher review, and helps the teacher choose the next intervention. Teachers can also set the tutor's class fit, support style, and guardrails on `/agents`, so the system adapts to how they want students to be helped, not just what content is covered.

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

Architecture direction: agent-native today, with future multi-agent role separation as a design direction rather than a current autonomy claim.

## MVP demo story

1. Teacher creates a Knowledge Pack.
2. Teacher generates questions from the pack.
3. Student studies with Tutor Agent grounded in the pack.
4. Teacher reviews diagnosis signals and recommendation context.
5. Teacher decides the next intervention using dashboard evidence.

Anchor case for the pitch:

- Grade 9 math teacher
- `contest-demo-quadratics`
- one common factoring and root-checking weakness pattern
- one teacher-reviewed remediation move

Preferred short version:

> One Grade 9 teacher prepares a quadratics Knowledge Pack, drafts one assessment, lets the student ask one grounded follow-up, then reviews one dashboard recommendation before choosing one bounded remediation step.

Official scope freeze:

- Core loop: `Knowledge Pack -> Assessment -> Tutor -> Diagnosis -> Intervention`
- Operator surface: the dashboard helps the teacher inspect and act on the loop
- Claim level: validated prototype, not classroom deployment
- Architecture claim: agent-native today, multi-agent by design as a future direction

Behavior-diff story for judges:

- `IDENTITY` changes who the tutor is serving: subject, grade band, tone, and language.
- `SOUL` changes how the tutor reacts when a student is wrong, stuck, or discouraged.
- `RULES` changes the classroom boundaries: for example, whether the tutor should withhold direct answers, how much hinting is allowed, and when to stop or escalate.
- The same student question can therefore receive a more encouraging scaffolded response in one class setup and a more Socratic push-back in another, without changing the underlying source material.

Bounded metric card for spoken Q&A:

- `1` anchor Knowledge Pack
- `2` verified demo sessions tied to that pack
- `2/2` verified sessions grounded in the same pack
- teacher-reviewed recommendation/intervention framing present

Do not translate that card into accuracy, learning-gain, or classroom-outcome claims.
