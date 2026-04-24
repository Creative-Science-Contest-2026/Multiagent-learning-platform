# T032 Knowledge Pack Versioning System

## Summary

- Added a lightweight versioning layer to teacher-pack metadata updates.
- Knowledge-pack config updates now auto-record `current_version` and append `version_history` entries when teacher-pack metadata actually changes.
- Existing knowledge packs remain backward-compatible when version metadata is absent.

## Architecture

```mermaid
flowchart LR
  TeacherEdit["Teacher updates KB metadata"] --> KnowledgeAPI["PUT /api/v1/knowledge/{kb}/config"]
  KnowledgeAPI --> DiffLogic["Compare current teacher-pack metadata vs new payload"]
  DiffLogic --> VersionEntry["Append version_history entry\nversion + updated_at + changed_fields"]
  VersionEntry --> KBConfig["kb_config.json teacher-pack metadata"]
  KBConfig --> KnowledgeList["GET /api/v1/knowledge/list"]
  KBConfig --> KnowledgeDetail["GET /api/v1/knowledge/{kb}"]
```

## Notes

- This slice stays backend-first and does not require a new knowledge-pack route family.
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` was updated for this change.
