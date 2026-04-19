# Task Packet: MVP Feature Pack 3 (Knowledge Marketplace + Student Learning + Vietnamese i18n)

**Date Created:** 2026-04-20  
**Status:** Not Started  
**Assigned Pod:** Pod A (Student/Teacher Features)  
**Owned Files:** See section below  
**Do-Not-Touch:** Apache 2.0 license, upstream HKUDS/DeepTutor attribution  

---

## Mission

Enhance the core teacher-student MVP flow by adding:
1. **Knowledge Pack Marketplace** — UI to browse and import teacher-shared (public/team) knowledge packs
2. **Student Learning Experience Enhancement** — Improve student interaction flow, visibility of learning progress, and context during tutoring
3. **Vietnamese Localization** — Full i18n coverage for Vietnamese (vi) language

These features complete the teacher MVP feedback loop and support Vietnamese users in the contest.

---

## Goals

### Goal 1: Knowledge Pack Marketplace
- **Objective:** Create a dedicated marketplace page to display public/team knowledge packs from other teachers.
- **Acceptance Criteria:**
  - New route `/marketplace` displays filterable list of knowledge packs with `sharing_status` = "public" or "team"
  - UI shows pack metadata: name, subject, grade, curriculum, owner, session_count
  - Students/teachers can preview and import public packs
  - Follows existing sidebar/card design patterns
  - Accessible from sidebar nav

### Goal 2: Student Learning Experience Enhancement
- **Objective:** Improve student visibility and engagement during assessment and tutoring.
- **Acceptance Criteria:**
  - Student sees progress indicator during assessment (e.g., X/N questions completed)
  - Tutoring session shows knowledge pack context/topic clearly
  - Assessment feedback includes score, correct/incorrect count, and recommended topics for review
  - Student chat/tutor interaction is more visually organized (e.g., role badges, clear Q&A separation)
  - Learning journey is traceable in memory/session history

### Goal 3: Vietnamese Localization (i18n)
- **Objective:** Full Vietnamese language support across frontend and backend prompts.
- **Acceptance Criteria:**
  - All UI strings in `web/locales/vi/app.json` (Vietnamese)
  - Teacher Dashboard labels, Knowledge Pack forms, Marketplace, and Assessment views are Vietnamese
  - LLM prompts in `deeptutor/agents/` have Vietnamese variants (zh/vi structure)
  - Student learning prompts (assessment, tutoring) support Vietnamese
  - Backend returns localized prompts based on user language preference
  - Fallback to English if Vietnamese not available

---

## Files

### Owned Files (create/modify as needed)

**Frontend (Web)**
- `web/locales/vi/app.json` — Vietnamese i18n strings
- `web/app/(utility)/marketplace/page.tsx` — Knowledge Pack Marketplace page (new route)
- `web/components/marketplace/` — Marketplace components (filters, pack cards, import modal)
- `web/lib/marketplace-api.ts` — Marketplace API client
- `web/components/student-learning/` — Student learning experience components (new)
- `web/app/(workspace)/assessments/page.tsx` — Student assessment flow (enhance)
- `web/app/(workspace)/tutoring/page.tsx` — Student tutoring flow (enhance)

**Backend (Python)**
- `deeptutor/api/routers/marketplace.py` — Marketplace API endpoints (new)
- `deeptutor/knowledge/marketplace.py` — Marketplace query logic (new)
- `deeptutor/agents/*/prompts/vi/` — Vietnamese prompt variants (create structure)
- `deeptutor/agents/question/prompts/vi/` — Vietnamese question generation prompts
- `deeptutor/agents/solve/prompts/vi/` — Vietnamese tutoring prompts
- `deeptutor/agents/guide/prompts/vi/` — Vietnamese guided learning prompts

**Documentation & Config**
- `docs/superpowers/pr-notes/2026-04-20-mvp-3-marketplace-i18n.md` — Architecture diagram + design notes
- `ai_first/architecture/MAIN_SYSTEM_MAP.md` — Update with marketplace and i18n layer
- `ai_first/daily/2026-04-20.md` — Daily progress log

### Do-Not-Touch Files
- All root-level license, config, and upstream credit files
- `deeptutor/core/` — Do not modify core protocols unless approved
- `deeptutor/runtime/` — Do not change registry or execution model
- Existing assessment/tutoring capability logic (enhance via new components only)

---

## Sequence & Checkpoints

### Checkpoint 1: Knowledge Pack Marketplace Setup (Days 1-2)
1. Create `/marketplace` route with API backend endpoints
2. Build marketplace UI (filters by subject, grade, owner)
3. Add import dialog to allow students to add public packs to their workspace
4. Test with demo data (create 2-3 public packs in seeded database)
5. **Verify:** API returns public/team packs, UI renders list, import works

### Checkpoint 2: Student Learning Experience (Days 3-4)
1. Add progress indicator to assessment flow
2. Enhance tutoring session layout with knowledge pack context badge
3. Improve assessment feedback display (score, breakdown, recommendations)
4. Add learning journey summary to student dashboard
5. **Verify:** Student sees clear progress, context, and feedback flow

### Checkpoint 3: Vietnamese i18n (Days 4-5)
1. Create Vietnamese locale file with full coverage
2. Add Vietnamese prompt variants to all agent modules
3. Update backend to serve localized prompts based on `?lang=vi`
4. Test translation completeness with smoke test
5. **Verify:** UI fully Vietnamese, LLM prompts are Vietnamese when requested

### Final: PR + Handoff (Day 5)
1. Create PR with all changes, link to task packet
2. Add architecture diagram to `docs/superpowers/pr-notes/`
3. Update `ai_first/architecture/MAIN_SYSTEM_MAP.md`
4. Update `ai_first/daily/2026-04-20.md` with completion notes
5. Merge and update `ai_first/EXECUTION_QUEUE.md`

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Vietnamese translation completeness | Use translation service or manual review; prioritize high-frequency UI strings first |
| Marketplace query performance with many packs | Index `sharing_status` in DB; paginate results |
| Student UX clarity | Mock up designs against existing patterns; test with demo user flow |
| i18n fallback logic | Implement graceful fallback to English; test both vi and en code paths |

---

## Success Metrics

- [ ] Marketplace page loads and displays ≥2 public packs
- [ ] Student can see assessment progress (e.g., "3/10 questions")
- [ ] Tutoring session clearly shows knowledge pack topic
- [ ] Assessment feedback is clear and actionable
- [ ] All UI strings render in Vietnamese when `lang=vi`
- [ ] LLM prompts include Vietnamese variants
- [ ] Demo smoke test passes with Vietnamese interface
- [ ] No regressions in existing English flow

---

## Notes for Next Worker

This task packet assumes the Knowledge Pack metadata structure is already in place (`sharing_status` field). If that's missing, coordinate with the Knowledge Pack Epic first.

Focus on iterative delivery: Marketplace MVP first, then UX enhancements, then i18n to avoid bottlenecks.

Use the daily log (`ai_first/daily/2026-04-20.md`) to track blockers and incremental progress.
