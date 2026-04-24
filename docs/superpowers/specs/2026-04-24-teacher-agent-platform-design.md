# Teacher-Agent Platform Design

Date: 2026-04-24
Status: Approved design baseline
Scope: Post-MVP product direction, AI-first operating doctrine, and a national-scale-ready coding philosophy for the teacher-defined agent platform

## Purpose

This design defines the next product direction after the current MVP backlog: a teacher-defined learning platform where teachers author their own teaching agents, students learn through those agents, and the system stays grounded in explicit pedagogy, evidence, and clean module boundaries.

The immediate target is not a true multi-agent system yet. The platform should start with a strong single-agent core and preserve the boundaries needed to split into specialized agents later.

## Product Thesis

The platform should support:

- Teacher-authored teaching agents
- Multiple student learning modes, not just chat
- Evidence-based observation and diagnosis
- Recommendation and intervention pipelines for teachers
- Marketplace sharing of agent templates and teaching packs
- Persistent AI-readable tracking so later AI workers can continue safely without losing context

## System Direction

### Current position

- Start as a configurable single-agent platform
- Each teacher defines a teaching agent spec
- Each student interacts with a personalized runtime view of that teacher agent
- The runtime may use teacher knowledge bases through RAG

### Long-term direction

The design should preserve clean boundaries so the platform can later evolve into a true multi-agent system with separate tutor, assessment, diagnosis, intervention, and marketplace agents.

## Evidence Pipeline

The platform should use a strict evidence pipeline:

1. `Observed`
   Direct evidence from a session, assessment, or interaction.
2. `Inferred`
   Controlled inference derived from observed evidence and always tagged with confidence.
3. `Recommended Action`
   Explicit next-step recommendations tied back to observed and inferred signals.

The system must never blur these three layers.

## Teaching Agent Pack

Teacher-defined agents should use a Markdown spec pack as the canonical source of truth. A form-based authoring UI may sit on top of it, but the Markdown pack remains the versionable artifact.

Recommended files:

- `IDENTITY.md`
- `SOUL.md`
- `CURRICULUM.md`
- `RULES.md`
- `ASSESSMENT.md`
- `WORKFLOW.md`
- `KNOWLEDGE.md`
- `MARKETPLACE.md`

### File purposes

`IDENTITY.md`
Teacher persona, subject, tone, language, and stable behavioral anchor.

`SOUL.md`
Teaching philosophy, pedagogy principles, emotional stance, and response habits.

`CURRICULUM.md`
Scope, topics, ordering, constraints, and teacher-owned knowledge goals.

`RULES.md`
Operational rules, refusal behavior, outside-scope handling, student-safety limits, and session limits.

`ASSESSMENT.md`
Quick checks, evidence thresholds, minimum rubric rules, and how assessment outcomes map to next actions.

`WORKFLOW.md`
Preferred instructional flow such as teach, guide, check, remediate, retry, advance.

`KNOWLEDGE.md`
Knowledge governance for the agent, especially the boundary between model prior knowledge and teacher-provided knowledge.

`MARKETPLACE.md`
Metadata for versioning, sharing, target audience, fit, and evidence notes.

## Runtime Model

Three runtime layers should stay separate:

- `Teacher Spec`
- `Student Profile`
- `Session State`

The runtime should assemble a personalized view from these layers rather than treating the whole system as one giant prompt.

Recommended prompt assembly:

- identity
- pedagogy
- rules
- workflow
- assessment policy
- knowledge policy
- relevant curriculum slice
- student profile summary
- current session goal

Only relevant curriculum and state slices should be loaded into the prompt.

## Student State Model

Recommended initial depth: medium, not minimal and not full learner modeling.

Persist after sessions:

- strengths
- weaknesses
- repeated mistakes
- topics covered
- learning preferences
- confidence level
- support level needed
- interventions tried
- whether those interventions seemed effective

Do not claim high-granularity mastery or retention models until a stronger measurement method exists.

## Knowledge and RAG Policy

RAG is a first-class part of the platform architecture, not an optional afterthought.

### Current repo context

The existing system already has:

- `rag` as a built-in tool
- request-level `knowledge_bases`
- knowledge base configs in `kb_config.json`
- tool-augmented chat where the model may call `rag`

What is missing is an agent-level knowledge contract.

### Required knowledge doctrine

Each teaching agent must define a `knowledge policy` in `KNOWLEDGE.md`.

Default recommendation: `kb_preferred`

Meaning:

- Use teacher knowledge bases when relevant material exists
- Allow controlled use of LLM prior knowledge when the teacher KB is silent or incomplete
- Distinguish clearly between grounded material and general model knowledge

Recommended sections in `KNOWLEDGE.md`:

- `knowledge_mode`
- `allowed_kbs`
- `source_priority`
- `grounding_rules`
- `citation_policy`
- `out_of_scope_policy`

Recommended default source priority:

`teacher_kb > curriculum excerpt > explicit teacher rules > llm prior knowledge`

Assessment, diagnosis, and teacher-facing recommendations should be more tightly grounded than general explanation.

## Product Pipeline

Track future product work by product stage:

- `authoring`
- `teaching`
- `observation`
- `assessment`
- `diagnosis`
- `intervention`
- `teacher_improvement`
- `marketplace_sharing`

This pipeline should drive backlog organization, task packets, and AI continuation.

## Coding and Architecture Doctrine

The platform must be easy to extend without cross-feature damage. This is mandatory for AI-first development and mandatory for any path toward national-scale use.

### Hard rules

1. Policy must stay separate from runtime logic.
2. Observation must stay separate from diagnosis.
3. Recommendation must stay separate from execution.
4. State must stay separate from inference.
5. RAG infrastructure must stay separate from pedagogy rules.
6. Marketplace logic must stay separate from tutor execution.
7. Prompt orchestration must stay separate from domain logic.
8. New features must use bounded modules with explicit input and output contracts.
9. Avoid god files, hidden shared state, and cross-feature if-else growth.
10. A local change should not silently alter another pipeline stage.

### Recommended future module boundaries

- `agent_spec`
- `prompt_assembly`
- `knowledge_policy`
- `student_model`
- `session_runtime`
- `observation_store`
- `assessment_engine`
- `diagnosis_engine`
- `intervention_engine`
- `teacher_insight_api`
- `marketplace_specs`

## Tracking and AI-First Continuation

All major product decisions should produce follow-up tracking in AI-readable form.

Recommended tracking buckets:

- `Now`
- `Next`
- `Later`

Each tracked item should include:

- `id`
- `title`
- `why`
- `scope`
- `depends_on`
- `evidence_or_method`
- `not_now_because`
- `next_read_path`

The repo should keep this tracking by product pipeline stage, not only by technical lane.

## Recommended Immediate Follow-up Structure

### Now

- Define the teacher-agent platform doctrine in `ai_first/`
- Add AI-first engineering philosophy for long-term scalability
- Begin a formal framework for evaluation dimensions and intervention mapping

### Next

- Design evaluation dimensions and evidence rules
- Design teacher-facing diagnosis and intervention pipeline
- Design authoring UX for the Markdown teaching-agent pack
- Design marketplace packaging and versioning for teaching-agent specs

### Later

- Split the single-agent runtime into specialized agents
- Add stronger learner modeling once reliable evidence methods exist
- Add richer analytics and intervention planning for teachers

## Open implementation direction

The next planning cycle should focus on:

1. evaluation dimensions
2. evidence sources
3. confidence rules
4. allowed diagnoses
5. allowed interventions

That planning should happen before implementation work starts on the teacher-agent platform.
