# Plan: F112 Provenance And Reason Trace Surfaces

## Step 1 — Type And Payload Audit

- inspect the current runtime-policy audit route and dashboard insight payloads
- define the exact read-only fields needed for student trust traces and small-group reason traces
- confirm the frontend API contracts to extend

## Step 2 — Backend Trust Payload Shaping

- extend `deeptutor/services/evidence/teacher_insights.py`
- add bounded `reason_trace` payloads for students and small groups
- keep all fields derived from existing evidence and recommendation payloads
- add or update dashboard API tests

## Step 3 — `/agents` Runtime Policy Audit Surface

- add runtime-policy-audit fetch helper to `web/lib/agent-spec-api.ts`
- render a read-only runtime policy audit panel in `SpecPackAuthoringTab`
- keep it capability-scoped and version-aware

## Step 4 — Dashboard Trust Surfaces

- extend `web/lib/dashboard-api.ts` with trust-trace types
- render a compact trust summary on student cards
- render a fuller trust trace on student detail
- replace generic small-group explanation copy with reason-trace fields

## Step 5 — Verification And Control-Plane Updates

- run targeted backend tests
- run targeted frontend lint
- update `MAIN_SYSTEM_MAP.md`
- add PR note with Mermaid diagram
- update `ACTIVE_ASSIGNMENTS`, `TASK_REGISTRY`, and daily log
