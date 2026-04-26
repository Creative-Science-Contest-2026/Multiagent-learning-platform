# F113 Capability-Wide Runtime Binding Coverage Design

## Metadata

- Task ID: `F113_CAPABILITY_WIDE_RUNTIME_BINDING_COVERAGE`
- Commit tag: `F113`
- Session bucket: `session-b-runtime-data`
- Owner scope: `deeptutor/capabilities/`, `deeptutor/services/runtime_policy/`, `deeptutor/services/session/turn_runtime.py`, bounded runtime-policy tests and docs
- Do-not-touch scope: teacher-facing dashboard UX, teacher workflow copy, Session A dashboard surfaces

## Goal

Extend the existing bounded runtime-binding proof from the unified Tutor `chat` path into additional shipped capability entry points so the repository can make a narrower but stronger claim: selected runtime capabilities consistently carry `agent_spec_id` through request validation, turn runtime, policy compilation, and capability execution.

## Current State

The repository already proves one live path:

- `turn_runtime` accepts `config.agent_spec_id` for `chat`
- `ChatCapability` compiles runtime policy from the referenced Agent Spec pack
- focused tests show a deterministic behavior difference in the unified Tutor turn path

Coverage is still partial:

- `deep_question` compiles assessment policy, but turn-level proof for `agent_spec_id` is not established
- `deep_solve` does not currently assemble runtime policy in its capability path
- `deep_research` currently validates its own request config and does not participate in bounded runtime-policy proof
- contest and architecture docs are calibrated to avoid overclaiming universal runtime binding

## Scope

### In Scope

- add capability-level runtime binding support for selected shipped entry points beyond `chat`
- preserve `agent_spec_id` as an allowed public config field for the covered capabilities
- prove request-path wiring through `TurnRuntimeManager` for each covered capability
- add or update bounded tests in:
  - `tests/core/`
  - `tests/api/test_unified_ws_turn_runtime.py`
  - `tests/services/runtime_policy/` if helper/compiler behavior changes
- add bounded docs proof and PR note describing exactly which capabilities are covered

### Out of Scope

- redesigning teacher-facing dashboard or `/agents` UX
- changing student-model or evidence semantics unless required for runtime binding tests
- universal binding claims across every plugin, router, or future capability
- spec version pinning, trace slicing, or teacher-facing trust surfaces from later tasks (`F114+`)

## Capability Coverage Decision

### Recommended Coverage Set

Cover these capabilities in `F113`:

- `chat`
- `deep_question`
- `deep_solve`

Do not expand `F113` to `deep_research` unless implementation shows it can consume teacher runtime policy without broadening semantics or requiring extra product decisions.

### Why This Set

- `chat` is the already-proved baseline and must remain green
- `deep_question` already assembles assessment policy, so this task can close the missing turn-path proof
- `deep_solve` is a shipped capability with a clear tutor-adjacent execution path and is the next strongest target for bounded binding
- `deep_research` is higher-risk because its pipeline is more autonomous and less obviously governed by the current teacher policy slices

## Design

### 1. Runtime Binding Contract

For each covered capability, the public request contract must accept `agent_spec_id` without relying on runtime-only bypasses.

Expected contract behavior:

- `chat` keeps `agent_spec_id`
- `deep_question` gains or preserves `agent_spec_id`
- `deep_solve` gains `agent_spec_id`
- capability config validation must still reject unrelated unknown fields

This keeps the binding path explicit and inspectable instead of hidden in ad hoc metadata mutation.

### 2. Turn Runtime Propagation

`TurnRuntimeManager.start_turn()` already validates capability config and passes the validated config into `UnifiedContext.config_overrides`.

`F113` should preserve that shape and prove it for each covered capability:

- incoming websocket turn payload contains `config.agent_spec_id`
- capability-specific validator accepts it
- `turn_runtime` passes it into `UnifiedContext.config_overrides`
- orchestrator and capability execution can resolve runtime policy from that config

No new side channel should be introduced if `config_overrides` already provides a sufficient contract.

### 3. Capability Policy Assembly

Covered capabilities should assemble teacher runtime policy in a capability-appropriate way:

- `chat` continues using `format_chat_system_context`
- `deep_question` continues using `format_assessment_context`
- `deep_solve` should assemble runtime policy before solver execution and inject a bounded policy context into the solving pipeline

For `deep_solve`, the policy effect should be minimal and explicit:

- compile runtime policy with `ensure_runtime_policy(context, "deep_solve")`
- inject a formatted policy block into the solver's conversation/runtime context without changing unrelated solver architecture
- emit a progress/debug event similar to other covered capabilities so tests can inspect the compiled policy path

The task does not need a new deep-solve-specific formatter unless the existing assessment/chat formatter is clearly wrong. Prefer the smallest formatter addition that matches current slices and use case.

### 4. Bounded Claim Surface

After `F113`, the repo may claim:

- bounded runtime-binding coverage exists for the unified `chat`, `deep_question`, and `deep_solve` turn paths

The repo must not claim:

- every capability, plugin, or entry point is runtime-bound
- teacher policy influences all research or visualization flows

Docs must remain precise enough that a reviewer can map each claim to tests.
