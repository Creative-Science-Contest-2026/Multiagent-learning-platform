# F115 Runtime Policy Audit Trace Design

## Metadata

- Task ID: `F115_RUNTIME_POLICY_AUDIT_TRACE`
- Commit tag: `F115`
- Session bucket: `session-b-runtime-data`
- Owner scope: `deeptutor/services/runtime_policy/`, bounded API/tests/docs
- Do-not-touch scope: teacher-facing dashboard UX, `/agents` UX, unrelated evidence features

## Goal

Make compiled runtime policy inspectable through a bounded backend contract so debugging, trust review, and future provenance surfaces can read what policy actually applied without scraping prompt text.

## Current State

- `F113` proved runtime binding reaches shipped turn paths.
- `F114` pinned the exact Agent Spec version per session so runtime policy can stay reproducible across turns.
- Runtime policy already serializes a debug block in-process, but that block is only visible inside runtime context and tests.
- There is no stable backend endpoint or helper dedicated to returning an audit trace for a selected runtime-policy snapshot.

## Problem

Without an inspectable audit trace, later debugging and teacher-trust work has to infer policy behavior indirectly from logs, prompt text, or code assumptions. That makes version pinning less useful because the pinned runtime state cannot yet be queried cleanly.

## Recommended Approach

Add a small runtime-policy audit service/helper plus a bounded backend read surface that returns:

- `agent_spec_id`
- `agent_spec_version` when available
- applied slices and raw slice text
- slice sources
- knowledge-policy mode
- teacher KB context summary
- debug fields already derived by the compiler

The route should compile or normalize runtime policy from an explicit request context rather than exposing turn history or session internals directly.

## Contract Shape

Recommended API shape:

- `GET /api/v1/agent-specs/{agent_id}/runtime-policy-audit`

Optional query parameters:

- `capability`
- `version`

Behavior:

1. `agent_id` is required.
2. `version` is optional; when present it should read the historical Agent Spec snapshot.
3. `capability` defaults to `chat` but can support the bounded shipped capabilities already covered by `F113`.
4. The response returns compiled runtime policy plus a compact audit envelope.

Example response shape:

```json
{
  "agent_spec_id": "fraction-coach",
  "agent_spec_version": 2,
  "capability": "chat",
  "runtime_policy": {
    "knowledge_policy": "kb_preferred",
    "source_priority": ["teacher_kb", "curriculum_excerpt", "teacher_rules", "llm_prior_knowledge"],
    "slices": {"SOUL": "...", "RULES": "..."},
    "sources": {"SOUL": "teacher_spec.SOUL", "RULES": "teacher_spec.RULES"},
    "debug": {
      "applied_slices": ["SOUL", "RULES"],
      "missing_slices": ["ASSESSMENT"],
      "slice_sources": {"SOUL": "teacher_spec.SOUL", "RULES": "teacher_spec.RULES"},
      "agent_spec_id": "fraction-coach",
      "agent_spec_version": 2,
      "has_teacher_kb_context": false
    }
  }
}
```

## Design Notes

### 1. Keep Audit Assembly Inside Runtime Policy Layer

Prefer adding a dedicated helper in `deeptutor/services/runtime_policy/` that builds a `RuntimePolicy` from explicit audit inputs. This keeps route code thin and avoids duplicating compiler assembly logic in the API layer.

### 2. Support Historical Versions

Reuse the `F114` version-fetching seam so the audit route can inspect a historical spec snapshot with `version=...`, not just the latest pack.

### 3. No Session-History Exposure

`F115` should not expose a general “inspect any past session” endpoint. The bounded contract is policy-centric, not turn-history-centric. Session-specific audit can be layered later once provenance surfaces are designed.

### 4. Stable Debug Envelope

The response should use the existing `runtime_policy.debug` model as the foundation so tests and later UI work can depend on one shape instead of ad hoc payloads.

## Testing Strategy

- runtime-policy service tests for audit payload assembly from latest and version-pinned Agent Specs
- API tests for the audit route success path and 404 behavior
- bounded assertions that no teacher-facing UI files are touched

## Success Criteria

1. an explicit backend route or helper can return an inspectable runtime-policy trace for an Agent Spec
2. the trace includes `agent_spec_id`, `agent_spec_version`, slices, sources, and debug fields
3. historical version inspection works when a version is requested
4. no teacher-facing dashboard or `/agents` UX files change
