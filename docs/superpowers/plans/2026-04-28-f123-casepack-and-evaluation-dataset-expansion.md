# F123 Implementation Plan

## Objective

Create a reusable validation casepack from existing diagnosis and evidence patterns, with lightweight proof tests and bounded documentation.

## Steps

1. Add the planning/control-plane checkpoint
   - claim the Session B assignment
   - move `F123` to `in-progress`
   - write the packet, spec, and plan
2. Build the casepack dataset
   - add a structured file under `ai_first/evidence/`
   - include bounded expected outcomes and traceability fields
   - keep the pack small and high-signal
3. Add proof tests
   - validate dataset structure
   - validate expected outcomes against the current diagnosis helper where appropriate
4. Update bounded docs proof
   - add a short casepack usage/readme doc
   - add a PR note with Mermaid
   - update `MAIN_SYSTEM_MAP.md` only if the evidence layer gains a durable new validation asset boundary
5. Verify
   - run targeted validation tests
   - run `python -m json.tool ai_first/TASK_REGISTRY.json >/dev/null`
   - run a registry consistency check
   - run `git diff --check`
