# PR Note: Risk Lane 4 Teacher Value Proposition

## Summary

This PR hardens the teacher-facing story for judges and voters by translating Agent Specs and the evidence loop into classroom outcomes instead of system jargon.

## What Changed

- rewrote `/agents` copy to explain class fit, support style, and guardrails in teacher language
- added explicit teacher-use-case framing to contest and pitch docs
- added a simple behavior-diff story for `IDENTITY`, `SOUL`, and `RULES`

## Main System Map

- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was not updated because no shipped route, capability, or data-flow behavior changed

## Diagram

```mermaid
flowchart LR
  Teacher["Teacher intent"]
  Specs["/agents: IDENTITY, SOUL, RULES"]
  Tutor["Tutor behavior"]
  Dashboard["Observed -> Inferred -> Action"]
  FollowUp["Teacher follow-up move"]

  Teacher --> Specs
  Specs --> Tutor
  Tutor --> Dashboard
  Dashboard --> FollowUp
```
