# PR Note — T021 Tutoring Session Replay Feature

## Summary

- Added tutoring replay links to dashboard activity rows.
- Added a dedicated dashboard replay page for tutoring sessions that renders the ordered conversation timeline with timestamps.
- Added regression coverage to ensure tutoring activity payloads expose a stable `replay_ref`.

## Architecture Impact

- No new backend route family was required.
- The dashboard activity payload now includes `replay_ref` for tutoring sessions, while replay content reuses the existing dashboard activity detail endpoint.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was not updated because this PR extends the existing dashboard review flow without changing system boundaries.

```mermaid
flowchart LR
  Dashboard[Dashboard activity list] --> ReplayRef[replay_ref]
  ReplayRef --> ReplayPage[/dashboard/sessions/:sessionId]
  ReplayPage --> DetailAPI[GET /api/v1/dashboard/:entryId]
  DetailAPI --> Timeline[Ordered session messages]
```

## Validation

- `python3 -m pytest tests/api/test_dashboard_router.py -q`
- `python3 -m py_compile deeptutor/api/routers/dashboard.py`
- `cd web && npm run build`

## Risks

- Replay currently renders message content as a text-first timeline and does not yet interpret richer event metadata or attachments.
