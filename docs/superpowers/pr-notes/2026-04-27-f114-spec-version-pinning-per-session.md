# PR Note: F114 Spec Version Pinning Per Session

- Task: `F114_SPEC_VERSION_PINNING_PER_SESSION`
- Scope: bounded session-level Agent Spec version pinning for runtime-policy reproducibility
- Main-system-map update: not required because no user-visible entry point or topology changed

## What Changed

- added `AgentSpecService.get_pack_version()` so runtime code can read an exact historical pack snapshot
- persisted a session-scoped `agent_spec_pin` the first time a turn resolves `config.agent_spec_id`
- taught runtime policy to prefer the pinned version over the mutable latest pack
- surfaced `agent_spec_version` in runtime-policy payload/debug metadata for bounded auditability
- added tests for historical snapshot fetch, session pin persistence, pinned runtime-policy compilation, and multi-turn reuse after the current pack changes

```mermaid
flowchart LR
  A["Turn request with agent_spec_id"] --> B["Resolve current Agent Spec pack"]
  B --> C["Persist session preferences.agent_spec_pin"]
  C --> D["Later turn in same session"]
  D --> E["Runtime policy loads pinned version"]
  E --> F["Stable teacher policy slices"]
```

## Validation

- `pytest tests/services/agent_spec/test_service.py tests/services/session/test_sqlite_store.py tests/services/runtime_policy/test_compiler.py tests/api/test_unified_ws_turn_runtime.py -q`
- `git diff --check`
