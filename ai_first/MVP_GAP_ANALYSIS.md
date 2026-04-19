# MVP Gap Analysis & Issue Audit Report
**Date:** 2026-04-20  
**Project:** Multiagent Learning Platform - VnExpress Science Innovation Contest 2026  
**Status:** Active Development  
**Total Issues Identified:** 27 (8 completed, 0 in-progress, 19 pending)

---

## Executive Summary

The MVP Feature Pack 3 (merged to main on 2026-04-20) successfully implements three major checkpoints:
1. **Knowledge Pack Marketplace** - Browse & filter UI complete, but **import functionality is placeholder only**
2. **Student Learning Experience** - Progress visualization complete, but **detailed feedback & recommendations missing**
3. **Vietnamese Localization** - UI translation done, but **LLM prompts not translated**

**Critical Gaps Identified:** 27 actionable issues across 6 categories:
- **Incomplete Features (5):** Marketplace import, assessment feedback, KB context, sharing UI, pack preview
- **Backend Services Missing (6):** Assessment analytics, recommendations engine, student dashboard, teacher analytics
- **UI/UX Improvements (7):** Error handling, mobile responsiveness, filtering, time tracking, follow-ups
- **i18n Completion (1):** Vietnamese prompts for all agents
- **Performance & Security (2):** Rate limiting, caching optimization
- **Advanced Features (6):** Versioning, learning paths, offline mode, replay, team sharing, adaptive difficulty

**Risk Level:** Moderate - Marketplace import placeholder is a blocker for contest demo

---

## Critical Priority Issues (P1-P3)

### P1 Issues: MVP Blockers (Do First)

#### T009: Implement Marketplace Pack Import
- **Status:** Not Started
- **Effort:** 4 hours
- **Blocker:** Marketplace import button currently shows success but doesn't copy pack
- **Scope:**
  - File: `web/app/(utility)/marketplace/page.tsx:60-75` - Replace `handleImportPack` placeholder
  - File: `deeptutor/api/routers/marketplace.py` - Add `POST /api/v1/marketplace/import/{pack_name}`
  - File: `web/lib/marketplace-api.ts` - Add `importMarketplacePack()` client function
- **Test Cases:**
  - Import creates copy in user's `knowledge_bases/` directory
  - Pack metadata, documents, config all copied
  - Success/error message shown
  - Imported pack appears in Knowledge Pack list
- **Notes:** Need to handle pack structure (metadata.yaml + document files)

**View Code:** [marketplace/page.tsx](web/app/(utility)/marketplace/page.tsx#L60-L75)

#### T010: Enhance Assessment Feedback with Analysis
- **Status:** Not Started
- **Effort:** 6 hours
- **Issue:** Assessment review shows score but lacks detailed topic breakdown and learning recommendations
- **Scope:**
  - File: `web/components/assessment/ProgressIndicator.tsx:40-80` - Expand recommendations section
  - New Backend: `deeptutor/api/routers/dashboard.py` - Add `GET /api/v1/dashboard/assessment-analysis/{session_id}`
  - Database: Extend `assessment_results` schema with `performance_by_topic`, `common_mistakes`
- **Missing Components:**
  - Topic-level performance breakdown
  - Mistake pattern analysis
  - Score-based learning paths
  - Visualization (pie chart/heat map)
- **Notes:** Requires LLM analysis of question-level performance

**View Code:** [ProgressIndicator.tsx](web/components/assessment/ProgressIndicator.tsx#L40-L80)

#### T011: Add KB Context Badges to Tutoring Session
- **Status:** Not Started  
- **Effort:** 2 hours
- **Issue:** Student doesn't see which knowledge pack a tutor response comes from
- **Scope:**
  - File: `web/components/chat/ChatMessageList.tsx` - Add KB badge display
  - Extract KB context from `UnifiedContext` in API response
- **Visual:** Show colored badge like "📚 Algebra Pack" near tutor messages
- **Notes:** Simple addition, high UX value

**View Code:** [ChatMessageList.tsx](web/components/chat/ChatMessageList.tsx)

#### T012: Teacher Knowledge Pack Sharing UI
- **Status:** Not Started
- **Effort:** 3 hours  
- **Issue:** Teachers can't mark packs as public/team/private in UI
- **Scope:**
  - File: `web/app/(workspace)/knowledge` - Add sharing settings panel
  - File: `deeptutor/api/routers/knowledge.py` - Extend pack update endpoint
  - Update: `pack_metadata.yaml` with `sharing_status`, `shared_with` fields
- **Missing UI:** Sharing dropdown (private/team/public), access list editor
- **Notes:** Prerequisite for marketplace import to work

#### T013: Marketplace Pack Preview Modal  
- **Status:** Not Started
- **Effort:** 3 hours
- **Issue:** Users can't preview pack contents before importing
- **Scope:**
  - File: `web/app/(utility)/marketplace/page.tsx` - Add modal component
  - Backend: `GET /api/v1/marketplace/{pack_name}/preview`
- **Preview Contents:** First 3 sample questions, learning objectives, document count
- **Notes:** Improves user confidence before import

---

### P2-P3 Issues: High Priority (Next Week)

#### T014: Student Progress Tracking Dashboard
- **Status:** Not Started | **Effort:** 5 hours | **Complexity:** High
- **Issue:** Students lack visibility into progress across all assessments
- **Scope:** Create `web/app/(workspace)/dashboard/student` with charts
- **Missing:** Timeline chart, topic mastery heatmap, learning streaks, recent assessments

#### T015: AI-Powered Assessment Recommendations  
- **Status:** Not Started | **Effort:** 6 hours | **Complexity:** High
- **Issue:** No personalized recommendations for next assessment
- **Scope:** New service `deeptutor/services/assessment/recommendation_engine.py`
- **Missing:** LLM-powered next-topic suggestion based on performance

#### T016: Marketplace Pack Ratings & Reviews
- **Status:** Not Started | **Effort:** 4 hours | **Complexity:** Medium
- **Issue:** No way for teachers to rate/review packs
- **Scope:** Add 5-star rating UI, backend rating storage
- **Missing:** Rating database table, display in pack cards

#### T017: Assessment History Filtering & Search
- **Status:** Not Started | **Effort:** 2 hours | **Complexity:** Low
- **Issue:** Teacher dashboard lacks filters for session history
- **Scope:** Add filter panel to dashboard, extend API query parameters
- **Missing:** Date range, KB, student, score filters

#### T018: Vietnamese LLM Prompt Variants
- **Status:** Not Started | **Effort:** 4 hours | **Complexity:** Medium
- **Issue:** Vietnamese UI works but all LLM responses are still in English
- **Scope:** Create `deeptutor/agents/*/prompts/vi/` YAML files
- **Missing:** Vietnamese prompts for solve, question generation, tutoring, research
- **Risk:** Contest judges may expect Vietnamese responses

---

## High Priority Issues (P4-P10)

#### T019: Marketplace Sorting Options
- **Effort:** 1.5 hours | **Quick Win**
- **Missing:** Sort by popularity, recent, rating, objectives

#### T020: Assessment Export to PDF
- **Effort:** 3 hours | **Medium**
- **Missing:** Export button in assessment review, PDF generation endpoint

#### T021: Session Replay/Timeline
- **Effort:** 3 hours | **Medium**
- **Missing:** Timeline view of tutoring conversation, useful for teacher review

#### T022: Error Boundary Handling  
- **Effort:** 2 hours | **Important for Stability**
- **Missing:** React error boundaries for marketplace, assessment pages

#### T023: Marketplace Caching & Pagination Optimization
- **Effort:** 2 hours | **Performance**
- **Missing:** Client-side cache, stale-while-revalidate pattern

#### T024: Teacher Team Invitation System
- **Effort:** 6 hours | **Complex**
- **Missing:** Team creation, email invitations, shared pack access control

#### T025: Assessment Difficulty Adaptive Adjustment
- **Effort:** 5 hours | **Advanced**
- **Missing:** CAT-style difficulty tracking and adjustment

---

## Medium Priority Issues (P11-P20)

#### T026: Mobile-First Responsive Design
- **Effort:** 1 hour | **Quick Win**
- **Issue:** Marketplace filters not well-optimized for mobile
- **Missing:** Responsive filter panel for small screens

#### T027: Teacher Analytics Dashboard
- **Effort:** 8 hours | **Complex**
- **Missing:** Comprehensive charts: student engagement, assessment trends, common difficulties

#### T028: API Rate Limiting & Throttling
- **Effort:** 2 hours | **Security**
- **Issue:** No protection against API abuse
- **Missing:** Rate limiter middleware, configure per endpoint

#### T029: Full-Text Search for Marketplace
- **Effort:** 3 hours | **Performance**
- **Missing:** Search across pack description, objectives, questions

#### T030: Assessment Time Tracking & Analytics
- **Effort:** 2 hours | **Easy Add**
- **Missing:** Track time per question, show time-based insights

#### T031: Smart Tutor Follow-Up Questions
- **Effort:** 3 hours | **UX**
- **Missing:** Tutor suggests 1-3 follow-up questions when student answers incorrectly

---

## Lower Priority Issues (P21-P27)

#### T032: Knowledge Pack Versioning System  
- **Effort:** 4 hours | **Maintenance**

#### T033: Learning Path Sequencing
- **Effort:** 6 hours | **Advanced**

#### T034: Batch Import Multiple Packs
- **Effort:** 2 hours | **Quick Add**

#### T035: Offline Mode for Downloaded Packs
- **Effort:** 6 hours | **Advanced**

---

## Issues by Category

### 1. Incomplete Feature Implementations (5 issues)
These are features that have UI/API stubs but missing core logic:

| Issue | Status | Hours | Risk |
|-------|--------|-------|------|
| T009: Marketplace Import | Placeholder | 4 | **CRITICAL** |
| T010: Assessment Feedback | Partial | 6 | **HIGH** |
| T011: KB Context Badges | Not Started | 2 | Medium |
| T012: Sharing UI | Not Started | 3 | High |
| T013: Pack Preview | Not Started | 3 | High |

**Action:** Fix T009 before contest submission (currently just shows fake success)

### 2. Missing Backend Services (6 issues)
New API endpoints and business logic needed:

| Service | Purpose | Hours | Files |
|---------|---------|-------|-------|
| Assessment Analytics | Score breakdown by topic | 6 | `deeptutor/api/routers/dashboard.py` |
| Student Dashboard | Progress tracking API | 5 | `deeptutor/api/routers/dashboard.py` |
| Recommendation Engine | AI-powered next assessment | 6 | `deeptutor/services/assessment/` |
| Teacher Analytics | Engagement & trend charts | 8 | `deeptutor/services/analytics/` |
| Team Management | Invitation & sharing | 6 | `deeptutor/api/routers/teams.py` |
| Learning Paths | Prerequisite sequencing | 6 | `deeptutor/services/learning_paths.py` |

### 3. UI/UX Issues (7 issues)
Frontend improvements and polish:

| Issue | Type | Hours | Impact |
|-------|------|-------|--------|
| T022: Error Boundaries | Stability | 2 | Prevents blank screens |
| T026: Mobile Responsive | UX | 1 | Better experience on phones |
| T017: Filter/Search | UX | 2 | Better dashboard usability |
| T019: Marketplace Sort | UX | 1.5 | Better pack discovery |
| T020: Export PDF | Feature | 3 | Teacher needs |
| T021: Session Replay | Teacher Tool | 3 | Useful for analysis |
| T031: Follow-Up Questions | Learning | 3 | Better pedagogy |

### 4. i18n Completion (1 issue)

| Issue | Status | Hours | Scope |
|-------|--------|-------|-------|
| T018: Vietnamese Prompts | Not Started | 4 | 4-5 agent prompt files |

**Impact:** Without this, Vietnamese students will get English responses from LLM

### 5. Performance & Security (2 issues)

| Issue | Type | Hours | Risk |
|-------|------|-------|------|
| T028: Rate Limiting | Security | 2 | **HIGH** - API abuse risk |
| T023: Caching | Performance | 2 | Better UX on slow networks |

### 6. Advanced Features (6 issues)

| Feature | Hours | Complexity | Value |
|---------|-------|-----------|-------|
| T024: Team Sharing | 6 | High | Collaboration |
| T025: Adaptive Difficulty | 5 | High | Better Learning |
| T032: Versioning | 4 | Medium | Maintenance |
| T033: Learning Paths | 6 | High | Smart Learning |
| T034: Batch Import | 2 | Low | Quick Win |
| T035: Offline Mode | 6 | High | Mobile Use |

---

## Risk Assessment Matrix

### High Risk - Must Address Before Contest

| Risk | Issue | Impact | Mitigation |
|------|-------|--------|-----------|
| Marketplace import is fake | T009 | Demo fails | Implement real import |
| Assessment feedback incomplete | T010 | Poor learning experience | Add analysis & recommendations |
| No Vietnamese responses | T018 | Judges expect Vietnamese | Translate LLM prompts |
| API can be DoS'd | T028 | Service downtime | Add rate limiting |
| App crashes on errors | T022 | Bad UX | Add error boundaries |

### Medium Risk - Nice to Have Soon

| Risk | Issue | Mitigation |
|------|-------|-----------|
| Marketplace slow with many packs | T023, T029 | Implement caching + search |
| Mobile UI breaks on small screens | T026 | Responsive redesign |
| No teacher analytics | T027 | Add analytics dashboard |

### Low Risk - Polish Items

| Risk | Issue | Mitigation |
|------|-------|-----------|
| Students don't understand KB context | T011 | Add badges |
| Teachers can't rate packs | T016 | Add rating system |

---

## Implementation Roadmap

### Phase 1: Critical Path (Next 2 weeks)
**Goal:** Fix blockers, get to contest-ready state
- [ ] T009: Marketplace Import Implementation (4h)
- [ ] T010: Assessment Feedback with Analysis (6h)
- [ ] T011: KB Context Badges (2h)
- [ ] T018: Vietnamese LLM Prompts (4h)
- [ ] T022: Error Boundaries (2h)
- [ ] T028: Rate Limiting (2h)

**Total:** ~20 hours | **Target:** 2026-05-04

### Phase 2: High Priority Features (Weeks 3-4)
- [ ] T012: Sharing UI (3h)
- [ ] T013: Pack Preview (3h)
- [ ] T014: Student Dashboard (5h)
- [ ] T015: Assessment Recommendations (6h)
- [ ] T016: Pack Ratings (4h)
- [ ] T017: Dashboard Filters (2h)
- [ ] T019: Marketplace Sort (1.5h)
- [ ] T020: PDF Export (3h)
- [ ] T021: Session Replay (3h)
- [ ] T023: Caching Optimization (2h)

**Total:** ~32.5 hours | **Target:** 2026-05-18

### Phase 3: Polish & Advanced Features (Weeks 5+)
- [ ] T024: Team Sharing (6h)
- [ ] T025: Adaptive Difficulty (5h)
- [ ] T026: Mobile Responsive (1h)
- [ ] T027: Teacher Analytics (8h)
- [ ] T029: Full-Text Search (3h)
- [ ] T030: Time Tracking (2h)
- [ ] T031: Follow-Up Questions (3h)
- [ ] T032: Versioning (4h)
- [ ] T033: Learning Paths (6h)
- [ ] T034: Batch Import (2h)
- [ ] T035: Offline Mode (6h)

**Total:** ~46 hours | **Target:** 2026-06-01

---

## File-Level Gaps

### Frontend Files Needing Work

| File | Issues | Status |
|------|--------|--------|
| `web/app/(utility)/marketplace/page.tsx` | T009, T013, T019, T024 | Partially done |
| `web/components/assessment/ProgressIndicator.tsx` | T010, T030 | Needs enhancement |
| `web/components/chat/ChatMessageList.tsx` | T011, T031 | Needs badges/follow-ups |
| `web/app/(workspace)/dashboard/page.tsx` | T014, T017, T027 | Needs student view & analytics |
| `web/app/(workspace)/knowledge/page.tsx` | T012, T016 | Needs sharing UI |

### Backend Files Needing Work

| File | Issues | Status |
|------|--------|--------|
| `deeptutor/api/routers/marketplace.py` | T009, T013, T019, T029 | Partial (list/detail OK) |
| `deeptutor/api/routers/dashboard.py` | T010, T014, T017, T020, T027 | Minimal implementation |
| `deeptutor/api/routers/knowledge.py` | T012, T016 | Needs sharing endpoints |
| `deeptutor/services/assessment/` | T010, T015, T025, T030 | Mostly missing |
| `deeptutor/agents/*/prompts/vi/` | T018 | Missing entirely |

### Database/Schema Issues

| Issue | Current | Missing |
|-------|---------|---------|
| Pack metadata | Basic | `sharing_status`, `ratings_count`, `download_count` |
| Assessment results | Sessions only | `performance_by_topic`, `time_per_question`, `mistake_patterns` |
| User data | Minimal | Team membership, preferences |

---

## Next Steps & Action Items

### Immediate (This Week)
1. **Review & Approve Audit** - Validate all 27 issues with team
2. **Create GitHub Issues** - Convert JSON registry to GitHub issues
3. **Assign Priority** - Confirm P1-P3 are top focus
4. **Estimate Stories** - Break down large tasks into 2-3 day chunks

### This Sprint (Next 2 Weeks)
1. Start T009 (Marketplace Import) - **BLOCKER**
2. Parallel: T010, T018, T022 (High impact)
3. Integrate into AI-first OPERATING_PROMPT.md
4. Update daily logs with progress

### Success Metrics
- [ ] T009 complete before contest submission
- [ ] Phase 1 complete: 6 critical tasks done
- [ ] Phase 2 started: First high-priority features in progress
- [ ] All GitHub issues created with acceptance criteria
- [ ] JSON registry updated daily with progress

---

## Appendix: JSON Task Registry

See: [ai_first/TASK_REGISTRY.json](ai_first/TASK_REGISTRY.json)

The JSON file contains:
- 35 detailed task objects with IDs, priorities, effort estimates, and file references
- Dependency graph showing task relationships
- Risk mitigation strategies
- Milestone definitions with target dates
- GitHub issue templates for quick issue creation

---

**Report Generated:** 2026-04-20  
**Next Review:** 2026-04-27 (weekly)  
**Prepared By:** GitHub Copilot MVP Audit Agent
