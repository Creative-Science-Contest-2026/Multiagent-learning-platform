# PR Architecture Note: Pod A Teacher Knowledge Pack MVP

## Summary

Adds the first teacher-owned Knowledge Pack metadata workflow. Teachers can create, edit, view, and persist pack metadata for subject, grade, curriculum, learning objectives, owner, and sharing status.

## Scope

Pod A-owned backend, frontend, and tests only:

- Knowledge API metadata validation and response exposure.
- Knowledge manager metadata normalization.
- Knowledge page create/edit metadata UI.
- Knowledge API client metadata types and update helper.
- Pod A tests for metadata persistence, validation, listing, and normalization.

## Mermaid Diagram

```mermaid
flowchart LR
  Teacher["Teacher"]
  KnowledgeUI["Knowledge Page"]
  KnowledgeAPI["web/lib/knowledge-api.ts"]
  Router["Knowledge Router"]
  Normalize["Normalize + Validate Metadata"]
  Config["KB Config Service"]
  Manager["KnowledgeBaseManager"]
  Responses["KB Detail/List Responses"]

  Teacher --> KnowledgeUI
  KnowledgeUI --> KnowledgeAPI
  KnowledgeAPI -->|PUT /api/v1/knowledge/{kb}/config| Router
  Router --> Normalize
  Normalize --> Config
  Config --> Manager
  Manager --> Responses
  Responses --> KnowledgeUI
```

## Architecture Impact

The Knowledge Pack product layer now has a concrete metadata create/edit/update flow. This changes the AI-first main system map by adding the Knowledge Pack metadata flow node.

## Data/API Changes

Knowledge Pack metadata fields are:

- `subject`
- `grade`
- `curriculum`
- `learning_objectives`
- `owner`
- `sharing_status`

The knowledge config endpoint accepts those fields, trims string values, normalizes learning objectives, validates sharing status as `private`, `team`, or `public`, and exposes metadata in KB detail/list responses.

## Tests

```bash
pytest tests/api/test_knowledge_router.py -v
pytest tests/knowledge -v
python3 -m compileall deeptutor
cd web && npm run build
```

## Main System Map Update

- [ ] Not needed, because:
- [x] Updated `ai_first/architecture/MAIN_SYSTEM_MAP.md`
