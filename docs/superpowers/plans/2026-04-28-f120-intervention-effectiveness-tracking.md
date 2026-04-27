# F120 Implementation Plan

## Objective

Add bounded intervention-effectiveness summaries to the evidence layer using existing intervention history and later observations, without claiming causal impact.

## Steps

1. Add failing tests first
   - service tests for `appears_helpful`, `mixed_or_unclear`, and `no_followup_signal`
   - bounded dashboard API assertions for attached effectiveness summaries
2. Isolate effectiveness logic
   - add a helper under `deeptutor/services/evidence/` that matches interventions to later same-topic evidence
   - keep windowing and labeling rules explicit and inspectable
3. Thread into existing payloads
   - attach optional summaries to existing intervention-history or small-group insight records
   - avoid any teacher-facing UI or workflow redesign
4. Update docs proof
   - write the PR note with Mermaid diagram
   - update `MAIN_SYSTEM_MAP.md` only if a new shared evidence seam becomes explicit
5. Verify
   - run targeted service and dashboard tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run a registry consistency check
   - run `git diff --check`
