# PR Note: Risk Lane 1 Runtime Binding Proof

## Summary

- allow the chat request contract to accept `agent_spec_id` in live turn config
- add focused tests proving the unified Tutor turn path carries that id into runtime policy assembly
- add a behavioral diff test for two contrasting Agent Spec packs and recalibrate contest wording to the bounded proof level

## Architecture

```mermaid
flowchart LR
  Request["WS start_turn config.agent_spec_id"]
  Runtime["TurnRuntimeManager"]
  Context["UnifiedContext.config_overrides"]
  Compiler["runtime_policy.ensure_runtime_policy"]
  Policy["Compiled teacher policy slices"]
  Chat["ChatCapability"]
  Output["Tutor behavior diff proof"]

  Request --> Runtime
  Runtime --> Context
  Context --> Compiler
  Compiler --> Policy
  Policy --> Chat
  Chat --> Output
```

## Main System Map

- Not updated. This lane proves and documents an existing runtime path; it does not introduce a new architectural boundary.

## Validation

- `pytest tests/services/runtime_policy/test_compiler.py tests/core/test_capabilities_runtime.py tests/api/test_unified_ws_turn_runtime.py -q`
- `git diff --check`
