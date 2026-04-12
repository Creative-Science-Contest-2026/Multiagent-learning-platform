# PR Architecture Note: AI-first Project OS

## Summary

Adds the repository operating layer for AI-first development: injected AI instructions, project memory files, architecture maps, task templates, competition evidence skeleton, and PR documentation rules.

## Scope

Documentation and workflow only. No runtime backend or frontend behavior changes.

## Mermaid Diagram

```mermaid
flowchart TD
  Human["Human team"] --> Direction["Ideas, feedback, final review"]
  Direction --> Specs["docs/superpowers/specs"]
  Specs --> Plans["docs/superpowers/plans"]
  Plans --> Tasks["docs/superpowers/tasks"]

  Tasks --> PodA["Feature Pod A branch"]
  Tasks --> PodB["Feature Pod B branch"]
  PodA --> PRA["Pull Request A"]
  PodB --> PRB["Pull Request B"]

  PRA --> Review["Human or AI review"]
  PRB --> Review
  Review --> Main["main branch"]

  Main --> Maps["ai_first/architecture/MAIN_SYSTEM_MAP.md"]
  Main --> Evidence["ai_first/evidence"]
  Main --> Daily["ai_first/daily"]
```

## Architecture Impact

Creates an explicit operating layer around the existing DeepTutor architecture. The runtime remains unchanged.

## Data/API Changes

No application data or API changes.

## Tests

Documentation verification:

```bash
rg -n "```mermaid|MAIN_SYSTEM_MAP|AI_OPERATING_PROMPT|Feature Pod" ai_first docs/superpowers .github
```

## Main System Map Update

- [ ] Not needed, because:
- [x] Updated `ai_first/architecture/MAIN_SYSTEM_MAP.md`
