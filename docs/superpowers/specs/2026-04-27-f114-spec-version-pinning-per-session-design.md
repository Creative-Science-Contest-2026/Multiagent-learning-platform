# F114 Spec Version Pinning Per Session Design

## Metadata

- Task ID: `F114_SPEC_VERSION_PINNING_PER_SESSION`
- Commit tag: `F114`
- Session bucket: `session-b-runtime-data`
- Owner scope: `deeptutor/services/agent_spec/`, `deeptutor/services/session/`, `deeptutor/services/runtime_policy/`, bounded tests/docs
- Do-not-touch scope: teacher-facing dashboard UX, Session A dashboard workflow files, broad `/agents` UI changes

## Goal

Pin each session to the exact teacher-spec version resolved at runtime so later turns, debugging, and audit surfaces do not drift if the teacher edits the underlying Agent Spec pack after the session has already started.

## Current State

- `F113` proves that `agent_spec_id` can reach runtime policy assembly on `chat`, `deep_question`, and `deep_solve`.
- Runtime policy currently resolves the latest Agent Spec pack by `agent_spec_id`.
- Agent Spec storage already versions packs under `agent_specs/<agent_id>/versions/vNNNN/`.
- Session persistence already stores session-level preferences and turn/event history, but it does not persist a stable spec-version pin that runtime policy can reuse.

## Problem

Without version pinning, two turns from the same session may resolve different spec content if the teacher edits the pack between turns. That breaks reproducibility for:

- teacher/runtime debugging
- trust/audit traces planned for later Session B tasks
- stable explanation of which policy actually governed a session

## Design

### 1. Session Pin Model

Add a session-level persisted pin with at least:

- `agent_spec_id`
- `agent_spec_version`
- optional `agent_spec_updated_at`

The pin belongs to session preferences/state, not turn-local metadata. It should be written the first time a runtime-bound turn resolves a teacher spec and then reused for future turns in the same session.

### 2. Resolution Rule

For covered runtime paths:

1. if a session already has a spec pin, runtime policy must resolve that exact version
2. if no pin exists and the request supplies `agent_spec_id`, resolve the current pack once and persist its version as the session pin
3. if no `agent_spec_id` is present, keep current fallback behavior and do not invent a pin

This rule keeps the first resolved version stable without changing unrelated sessions.

### 3. Agent Spec Service Contract

Add a bounded way to read a specific version snapshot from `versions/vNNNN/` without mutating the current pack API. The minimal contract can be one of:

- `get_pack_version(agent_id, version)`
- or `get_pack(agent_id, version=...)`

Recommendation: add a dedicated version-fetch helper so the default `get_pack()` remains clearly “latest/current”.

### 4. Runtime Policy Contract

Extend runtime policy metadata/debug output so it reports:

- `agent_spec_id`
- pinned `agent_spec_version`
- whether the current turn reused an existing session pin or created a new one

Do not change teacher-facing claim surfaces in this task. This is runtime provenance groundwork.

### 5. Session Store Contract

Persist the spec pin inside session preferences JSON or a bounded session-state field already owned by Session B.

Recommendation: use session preferences JSON so pinning is session-scoped, lightweight, and does not require a new table.

Expected shape:

```json
{
  "capability": "chat",
  "agent_spec_pin": {
    "agent_spec_id": "strict-fractions",
    "version": 2,
    "updated_at": "2026-04-26T10:15:00Z"
  }
}
```

### 6. Scope Boundary

`F114` should not add UI for version history or teacher-facing provenance. It should only make the runtime/session contract reproducible so later tasks can expose it safely.

## Testing Strategy

- service tests for loading a specific Agent Spec version snapshot
- session-store tests proving the pin is persisted and readable
- runtime-policy tests proving an existing pin overrides later “latest” edits
- unified-turn tests proving the first runtime-bound turn creates the pin and later turns reuse it

## Success Criteria

1. the first runtime-bound turn in a session can persist a spec-version pin
2. later turns in the same session reuse that exact version even if the current pack has changed
3. runtime-policy metadata/debug output identifies the pinned version
4. no teacher-facing dashboard or `/agents` UX files are modified
