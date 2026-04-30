# 2026-04-30 Class Tutor Pack Flow

- Task ID: `UI_CLASS_TUTOR_PACK_FLOW`
- Commit tag: `UI-TUTOR-PACK`
- Branch: `fix/class-tutor-pack-flow`
- Worktree: `.worktrees/fix-class-tutor-pack-flow`
- Status: `in_progress`

## Goal

Refactor the class tutor setup screen so it reads as the next step after Knowledge Pack setup, with each class tutor visibly bound to one active Knowledge Pack at a time.

## User-visible outcome

- The class tutor screen no longer feels like a separate configuration island.
- Teachers can immediately see which Knowledge Pack a class tutor belongs to.
- The tutor setup form reads like “define how this tutor teaches this pack,” not as a free-floating agent editor.
- Teachers can choose or change the linked Knowledge Pack without leaving the tutor flow.

## Owned files

- `web/app/(workspace)/agents/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/components/agents/class-tutor-pack-presenters.ts`
- `web/lib/agent-spec-api.ts`
- `web/lib/knowledge-api.ts`
- `web/locales/en/app.json`
- `web/locales/vi/app.json`
- `web/tests/contest-terminology.test.ts`
- `web/tests/class-tutor-pack-presenters.test.ts`
- `deeptutor/api/routers/agent_specs.py`
- `deeptutor/services/agent_spec/service.py`
- `tests/api/test_agent_specs_router.py`
- `tests/services/agent_spec/test_service.py`
- `ai_first/ACTIVE_ASSIGNMENTS.md`
- `ai_first/daily/2026-04-30.md`
- `docs/superpowers/tasks/2026-04-30-class-tutor-pack-flow.md`
- `docs/superpowers/specs/2026-04-30-class-tutor-pack-flow-design.md`
- `docs/superpowers/pr-notes/2026-04-30-class-tutor-pack-flow.md`

## Do-not-touch

- `web/app/(utility)/knowledge/page.tsx` unless the approved design later expands scope
- `web/app/(workspace)/agents/[botId]/chat/page.tsx`
- lockfiles and generated files

## Required code reading

- `web/app/(workspace)/agents/page.tsx`
- `web/components/agents/SpecPackAuthoringTab.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- `web/lib/agent-spec-api.ts`
- `web/lib/knowledge-api.ts`
- `deeptutor/api/routers/agent_specs.py`
- `deeptutor/services/agent_spec/service.py`
- `tests/api/test_agent_specs_router.py`
- `tests/services/agent_spec/test_service.py`

## Design before implementation

### Current behavior

- The class tutor route and the Knowledge Pack route use the same contest narrative, but they still feel like separate tools.
- `SpecPackAuthoringTab` is structured like a generic spec editor rather than a teacher-facing “configure tutor for this pack” flow.
- The current tutor summary rail shows tone, language, and runtime policy information, but it does not clearly anchor the tutor to one Knowledge Pack.
- The Knowledge Pack route already carries a wizard-first mental model, but that model does not visibly continue inside the class tutor route.

### Intended behavior change

- The class tutor page should read as step 2 after Knowledge Pack setup.
- Each class tutor should bind to exactly one active Knowledge Pack at a time in this lane.
- The selected Knowledge Pack should be visible in the header, left rail, and teacher-facing summary of the tutor setup flow.
- The teacher should be able to choose or change the linked pack inside the tutor screen without feeling kicked into a separate unrelated tool.
- The pack link must persist through the existing agent-spec create/update/list/detail APIs.

### Candidate approaches

1. **Add one small “linked pack” badge only**
   - Pros: minimal change.
   - Cons: does not solve the disconnected flow or the editor-heavy layout.

2. **Keep `/agents`, but redesign it as step 2 of the Knowledge Pack flow**
   - Pros: fixes the mental model while staying inside a bounded route and likely existing frontend contracts.
   - Cons: requires meaningful rework of `SpecPackAuthoringTab`.

3. **Move tutor configuration inside `/knowledge`**
   - Pros: most seamless wizard.
   - Cons: wider route and state scope than this lane should own.

### Chosen approach

- Use **Approach 2**.
- Keep `/agents` as the tutor route, but make it clearly inherit the Knowledge Pack setup flow and treat the linked pack as the first-class object the tutor is being configured for.
- Persist only a thin `linked_knowledge_pack` reference in agent-spec metadata; do not widen into multi-pack tutor orchestration.

### Expected impact surface

- Likely change:
  - `web/app/(workspace)/agents/page.tsx`
  - `web/components/agents/SpecPackAuthoringTab.tsx`
  - locale keys and one or more focused UI tests if new presenter helpers or summaries are introduced
  - `web/lib/agent-spec-api.ts`
  - `deeptutor/api/routers/agent_specs.py`
  - `deeptutor/services/agent_spec/service.py`
  - `tests/api/test_agent_specs_router.py`
  - `tests/services/agent_spec/test_service.py`
- Reviewed but expected unchanged:
  - tutor runtime chat page
  - backend runtime policy compiler
  - Knowledge Pack route behavior

### Validation paths

- The tutor header makes the route read like step 2 after Knowledge Pack.
- The selected Knowledge Pack is visible and changeable from inside the tutor setup surface.
- The tutor list and summary rail both reflect the linked pack.
- The lane does not widen into a full route merge or backend workflow rewrite.
- The linked pack survives save, reload, and list/detail API reads.

## Acceptance criteria

- A teacher can tell which Knowledge Pack a class tutor belongs to without reading raw IDs.
- The tutor setup no longer reads like a separate generic file editor.
- The page hierarchy makes “choose pack, then define teaching style” visually obvious.
- The flow remains bounded to the existing class tutor route in this lane.
- Saving a tutor preserves exactly one linked Knowledge Pack reference.

## Validation

- `pytest tests/services/agent_spec/test_service.py tests/api/test_agent_specs_router.py -q`
- `cd web && node --test tests/contest-terminology.test.ts tests/class-tutor-pack-presenters.test.ts`
- `cd web && npx eslint "app/(workspace)/agents/page.tsx" "components/agents/SpecPackAuthoringTab.tsx"`
- `cd web && npm run build`
- `git diff --check`

## PR architecture note

- Must include Mermaid diagram.
- Update `ai_first/architecture/MAIN_SYSTEM_MAP.md` only if the implementation changes the teacher-facing route or step relationship in a way that should be reflected in the main system map.

## Implementation notes

- Added a thin `linked_knowledge_pack` field to the agent-spec router, service metadata, list payload, detail payload, and version snapshots.
- Kept the stored relationship intentionally narrow: one tutor references one Knowledge Pack by pack name only.
- Reframed `/agents` so the tutor authoring flow reads as step 2 after Knowledge Pack setup instead of a generic file editor.
- Added a pure presenter helper for linked-pack summaries so teacher-facing copy and status logic stay centralized.
- Kept `/knowledge`, tutor runtime chat, and the runtime policy compiler out of scope.

## Validation results

- `pytest tests/services/agent_spec/test_service.py tests/api/test_agent_specs_router.py -q`
- `cd web && node --test tests/contest-terminology.test.ts tests/class-tutor-pack-presenters.test.ts`
- `cd web && npx eslint 'app/(workspace)/agents/page.tsx' 'components/agents/SpecPackAuthoringTab.tsx' 'components/agents/class-tutor-pack-presenters.ts' 'lib/agent-spec-api.ts' 'tests/contest-terminology.test.ts' 'tests/class-tutor-pack-presenters.test.ts'`
- `cd web && npm run build`
- `git diff --check`

## Handoff notes

- `web/node_modules` had to be installed with `npm ci` inside this worktree before lint/build verification could run.
- `web/next-env.d.ts` was touched by Next during build and then restored to the tracked snapshot so the lane stays free of generated-file drift.
