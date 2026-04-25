# Engineering Philosophy

This file defines the long-form engineering doctrine for the AI-first learning platform.

The goal is not just to make the project work once. The goal is to make it expandable, reviewable, and safe for repeated AI-driven evolution toward a much larger future system.

## Core principle

Build every feature so it can be changed later without forcing unrelated features to move with it.

If a feature requires code overlap, hidden coupling, or cross-cutting edits to unrelated modules, the architecture is not ready for that feature yet.

## Non-negotiable outcomes

The codebase must remain:

- readable by humans
- operable by future AI workers
- safe for incremental changes
- testable in bounded slices
- replaceable at module boundaries
- capable of growth toward a national-scale platform

## Doctrine

### 1. Bounded ownership

Every feature must have an explicit ownership boundary.

- A worker should know which files they own.
- A change should not spill into neighboring modules unless the task scope is updated first.
- Shared infrastructure should stay small and explicit.

### 2. Specification before behavior

Pedagogical behavior belongs in specifications and policies before it belongs in code.

- Teacher identity belongs in agent specs.
- Teaching philosophy belongs in agent specs.
- Knowledge rules belong in agent specs.
- Assessment and intervention rules belong in domain policy files and contracts.

Do not bury behavior in scattered prompt strings or ad hoc branching logic.

### 3. Clean separation of layers

The platform should keep these layers distinct:

- policy
- runtime orchestration
- retrieval
- state
- observation
- diagnosis
- recommendation
- execution
- marketplace packaging

If one layer starts directly mutating or deciding for another without a contract, refactor before scaling the feature.

### 4. Observation is not diagnosis

Direct evidence and inferred interpretation are not the same thing.

- observed data must remain raw enough to audit
- inferences must be confidence-tagged
- recommendations must point back to evidence

No module may collapse these into one vague object.

### 5. Recommendation is not execution

Recommendation engines may advise action.
Execution layers may carry out action.

These should be separate so the platform can:

- explain what was recommended
- review what was actually executed
- test each layer independently
- add teacher approval gates later

### 6. RAG is infrastructure, not pedagogy

Retrieval exists to provide grounded knowledge access.
It does not define teaching philosophy.

- RAG components should handle indexing, retrieval, routing, and source metadata.
- Pedagogy components should decide when grounding is required.
- Knowledge governance should be explicit in agent policy.

### 7. Prompt orchestration is not domain logic

Prompt assembly, tool routing, and model interaction are orchestration concerns.

Assessment rules, diagnosis criteria, intervention mapping, and teacher insight logic are domain concerns.

Keep them separate so model changes do not silently rewrite product rules.

### 8. Small modules over god files

Avoid:

- giant service files
- giant page components
- giant prompt builders
- giant utility modules

Prefer:

- narrow modules
- explicit names
- one-directional dependencies
- focused contracts

### 9. No hidden side effects

Modules should not mutate global state or unrelated domain objects without an explicit contract.

Examples to avoid:

- assessment flow quietly editing student profile without a write contract
- recommendation flow auto-assigning work without an execution step
- chat runtime rewriting diagnosis state directly

### 10. Local change safety

A change for one pipeline stage should not silently break another stage.

Before adding a feature, ask:

- what module owns this behavior
- what data contract it uses
- what can break if it changes
- whether the boundary is clear enough for isolated testing

### 11. Version everything important

The system must be able to evolve without ambiguous hidden behavior.

Version:

- teaching-agent specs
- marketplace templates
- assessment policies
- intervention rules
- student-model structures

### 12. AI-maintainable architecture

The repo should be organized so future AI workers can continue safely.

That means:

- short read paths
- explicit operating docs
- clear task packets
- well-named modules
- limited side effects
- preserved context in `ai_first/`

## Anti-patterns

Avoid these patterns:

- feature logic copied across pages and routers
- one service owning unrelated business rules
- prompts containing product policy with no source document
- student state mutated from many entry points with no schema
- marketplace data model coupled directly to runtime tutoring state
- assessment, diagnosis, and intervention jammed into one response object

## Good architecture signals

You are probably on the right path if:

- a worker can explain a module without reading its internals
- a module can be replaced without breaking unrelated stages
- evidence, diagnosis, and action are separately inspectable
- teacher agent specs can evolve without rewriting runtime internals
- retrieval policy can change without rewriting pedagogy logic
- marketplace sharing can expand without touching core student state

## Future-facing intent

The immediate product may start as a strong single-agent system.

The codebase should still preserve the option to grow into:

- specialized tutor agents
- assessment agents
- diagnosis agents
- intervention-planning agents
- teacher-authoring assistants
- marketplace curation agents

That future becomes realistic only if boundaries are protected now.
