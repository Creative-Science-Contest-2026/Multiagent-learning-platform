# MVP Feature Pack 3 - Architecture Note

**PR:** Feature: Knowledge Marketplace + Student Learning + Vietnamese i18n  
**Branch:** `pod-a/marketplace-i18n-mvp`  
**Task Packet:** [docs/superpowers/tasks/2026-04-20-mvp-feature-pack-3.md](../tasks/2026-04-20-mvp-feature-pack-3.md)

## Overview

This PR delivers 3 interconnected features that enhance DeepTutor's learning experience and multi-language support:

1. **Knowledge Pack Marketplace** — Browse and import teacher-shared learning materials
2. **Student Learning Enhancement** — Visual progress tracking and personalized feedback
3. **Vietnamese Localization** — Full i18n support for Vietnamese-speaking users

---

## Architecture Changes

### System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client (Next.js 16)                          │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │  Marketplace   │  │   Assessment   │  │   Settings     │    │
│  │     Page       │  │  Review Page   │  │     Page       │    │
│  │ (/marketplace) │  │  (with new     │  │ (language      │    │
│  │                │  │   components)  │  │  picker)       │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│          ↓                   ↓                    ↓              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           i18n System (i18next)                        │    │
│  │  ✅ English | 中文 | Tiếng Việt                       │    │
│  │  Locales: vi/app.json, vi/common.json                 │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                          │
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │  /marketplace        │  │  /settings           │             │
│  │  - /list             │  │  - language: vi, zh, en            │
│  │  - /{pack_name}      │  │  - returns localized config        │
│  │                      │  │                      │             │
│  └──────────────────────┘  └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
         ↓                                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Service Layer (Python)                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PromptManager (Unified)                               │   │
│  │  ✅ LANGUAGE_FALLBACKS: vi → en                        │   │
│  │  ✅ Tool prompts: vi labels in phase_labels            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Language Support System                               │   │
│  │  - parse_language() → handles vi/vietnamese codes      │   │
│  │  - normalize_language() → vi preference handling       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  Data Layer (Knowledge Bases)                   │
│  Knowledge Packs (filtered by sharing_status)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Feature Breakdown

### 1. Knowledge Pack Marketplace

**New Files:**
- `deeptutor/api/routers/marketplace.py` — API endpoints for marketplace operations
- `web/lib/marketplace-api.ts` — Client functions for marketplace queries
- `web/app/(utility)/marketplace/page.tsx` — Marketplace browsing UI

**API Endpoints:**
```
GET /api/v1/marketplace/list
Query params: search, subject, owner, sharing_status, limit, offset

GET /api/v1/marketplace/{pack_name}
Returns: pack details with verification of access rights
```

**Features:**
- Real-time search across packs
- Multi-filter support (subject, owner, sharing status)
- Pagination (20 packs/page)
- Pack card layout with metadata display
- Import button (phase 2: integration with KB import flow)

---

### 2. Student Learning Experience Enhancement

**New Components:**
- `web/components/assessment/ProgressIndicator.tsx` — Visual score progress with recommendations
- `web/components/assessment/LearningJourneySummary.tsx` — Session tracking and topic badges

**Modified:**
- `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx` — Integrated new components

**Features:**
- **Progress Visualization**
  - Score percentage bar with color coding (green/yellow/red)
  - Score rating badge (Excellent/Good/Fair/Needs improvement)
  - Correct/Incorrect/Total breakdown

- **Personalized Recommendations**
  - Score-based feedback (< 75% → review topics, ≥ 90% → explore advanced)
  - Related knowledge base suggestions
  - Next steps guidance

- **Learning Journey Context**
  - Session date and time spent tracking
  - Mastered topics display
  - Recommended topics for exploration
  - Learning path suggestions

---

### 3. Vietnamese Localization (i18n)

**Scope:**
- **Frontend:** Full Vietnamese UI translation
- **Backend:** Language preference support across all services
- **Prompts:** Vietnamese variants for LLM interactions

**New Files:**
- `web/locales/vi/app.json` (180+ UI strings)
- `web/locales/vi/common.json` (core translations)

**Modified Services:**
- `web/i18n/init.ts` — Added Vietnamese resource bundle
- `deeptutor/api/routers/settings.py` — `language: Literal["en", "zh", "vi"]`
- `deeptutor/services/config/loader.py` — Enhanced `parse_language()` for Vietnamese
- `deeptutor/services/prompt/manager.py` — Fallback chain: `vi → en`
- `deeptutor/tools/prompting/__init__.py` — Tool prompt labels in Vietnamese

**Language Normalization:**
```python
# Supported formats:
parse_language("vi") → "vi"
parse_language("vietnamese") → "vi"
parse_language("VN") → "vi"
```

**i18n Fallback Chain:**
```
Vietnamese (vi) → English (en)
English (en) → Chinese (zh)
Chinese (zh) → English (en)
```

---

## Data Flow Example

### Marketplace Browse (English User)

```
User clicks /marketplace
         ↓
Next.js page loads with i18n context (en)
         ↓
listMarketplacePacks() → GET /api/v1/marketplace/list
         ↓
FastAPI router queries knowledge base
         ↓
Returns: [{ name, subject, owner, grade, objectives }]
         ↓
UI renders pack cards with English labels
```

### Assessment Review (Vietnamese User)

```
Student completes assessment
         ↓
User language: vi (from AppShellContext)
         ↓
i18n loads vi/app.json translations
         ↓
Assessment page renders:
  - ProgressIndicator (labels in Vietnamese)
  - LearningJourneySummary (labels in Vietnamese)
  - Recommendations (Vietnamese text)
         ↓
Backend prompt calls use vi language preference
  (via PromptManager fallback: vi → en)
```

---

## Testing Checklist

- [x] Marketplace API returns correct pack structure
- [x] Marketplace UI renders with filters and pagination
- [x] ProgressIndicator displays correctly with score ranges
- [x] LearningJourneySummary shows session metadata
- [x] Vietnamese locale files have full key coverage
- [x] Settings page language picker includes Vietnamese
- [x] Language normalization works for all variants (vi, vietnamese, VN)
- [x] i18n fallback chain works (vi → en)
- [x] Backend accepts "vi" in language settings
- [x] Tool prompts include Vietnamese labels

---

## Integration Points

### Marketplace Integration
- **Phase 2:** Connect import button to KB import workflow
- **Phase 2:** Add pack preview/details modal
- **Future:** Add ratings/reviews system

### Learning Experience Integration
- **Current:** Assessment review page
- **Phase 2:** Extend to tutoring session dashboards
- **Phase 2:** Integrate progress tracking across multiple sessions

### i18n Integration
- **Current:** UI and prompt system
- **Phase 2:** API responses with localized descriptions
- **Phase 2:** User notifications and emails in selected language

---

## Performance Considerations

- Marketplace queries filtered by `sharing_status` for reduced result sets
- i18n resources loaded once at app initialization
- PromptManager caching still effective with Vietnamese fallback chain
- No breaking changes to existing API contracts

---

## Commits in This PR

1. `b905e57` — feat: add knowledge pack marketplace MVP
2. `0a4b686` — feat: complete checkpoints 2 and 3
3. `2965709` — docs: update daily log with checkpoints 2 & 3 completion

---

## Related Documentation

- Task Packet: [2026-04-20-mvp-feature-pack-3.md](../tasks/2026-04-20-mvp-feature-pack-3.md)
- Daily Log: [ai_first/daily/2026-04-20.md](../../ai_first/daily/2026-04-20.md)
- Main System Map: [ai_first/architecture/MAIN_SYSTEM_MAP.md](../../ai_first/architecture/MAIN_SYSTEM_MAP.md)

