# Task Packet: T009 Marketplace Pack Import Implementation

**Date:** 2026-04-20  
**Feature Pod:** pod-a/marketplace-pack-import  
**Priority:** P1 CRITICAL  
**Status:** Planning → Implementation  
**Effort:** 4 hours estimated  

---

## Overview

Replace placeholder marketplace pack import with real implementation that copies knowledge packs to user workspace.

**Current State:** Import button shows success message but doesn't actually import pack  
**Target State:** Clicking import copies pack metadata and documents to user's knowledge_bases directory

---

## Problem Statement

Users can browse marketplace packs but import button is non-functional:
- Shows fake success after 1-second delay
- Doesn't copy pack files to workspace
- Makes marketplace feature appear to work during demo but fails in real use
- **Blocks contest demo** - judges can't actually import packs

### Evidence

**File:** `web/app/(utility)/marketplace/page.tsx` lines 60-75
```tsx
const handleImportPack = async (packName: string) => {
  setImporting(packName);
  try {
    // Placeholder: In a real scenario, this would copy the pack to the user's workspace
    // For now, we just show a success message
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setImportSuccess(packName);
    setTimeout(() => setImportSuccess(null), 3000);
```

---

## Acceptance Criteria

- [ ] **API Endpoint Created**: `POST /api/v1/marketplace/import/{pack_name}`
  - Validates pack exists in marketplace
  - Copies pack to user's knowledge_bases directory
  - Returns success/error with proper HTTP status
  - Handles edge cases (pack already imported, permission denied, disk full)

- [ ] **Frontend Integration**: Replace placeholder in `handleImportPack`
  - Call new API endpoint with pack name
  - Show proper loading indicator during import
  - Handle errors with user-friendly messages
  - Show success confirmation
  - Refresh pack list or navigate to imported pack

- [ ] **API Client Function**: Add `importMarketplacePack()` to `web/lib/marketplace-api.ts`
  - Takes pack name as parameter
  - Makes POST request with error handling
  - Returns response with imported pack details

- [ ] **Testing**: Verify end-to-end import flow
  - Browse marketplace
  - Click import button
  - See loading state
  - Confirm import completes
  - Check imported pack appears in Knowledge Pack list
  - Verify pack documents are accessible in workspace

---

## Files to Modify

### Backend
| File | Work | Lines |
|------|------|-------|
| `deeptutor/api/routers/marketplace.py` | Add import endpoint | ~30-40 lines |
| `deeptutor/api/main.py` | Verify marketplace router mounted | ~2 lines verify |
| `deeptutor/services/knowledge/pack_manager.py` | Add copy/import logic | ~50-60 lines |

### Frontend
| File | Work | Lines |
|------|------|-------|
| `web/app/(utility)/marketplace/page.tsx` | Implement real import handler | ~15-20 lines |
| `web/lib/marketplace-api.ts` | Add API client function | ~10-15 lines |

### No Changes
- Tests (existing placeholder test structure sufficient for now)
- Database schema (use existing pack metadata structure)
- i18n (use existing marketplace translations)

---

## Implementation Breakdown

### Step 1: Backend API Endpoint (90 min)

**File:** `deeptutor/api/routers/marketplace.py`

Create endpoint:
```python
@router.post("/import/{pack_name}")
async def import_marketplace_pack(
    pack_name: str,
    request: Request,
) -> dict:
    """Import marketplace pack to user's workspace."""
    # 1. Get user context from session
    # 2. Verify pack exists in marketplace
    # 3. Check pack is shareable (sharing_status != "private")
    # 4. Call pack_manager.import_pack(pack_name, user_id)
    # 5. Return success with imported pack metadata
```

**Logic:**
1. Validate pack_name exists in marketplace metadata
2. Check pack sharing_status is "public" or "team" (not "private")
3. Get destination path: `knowledge_bases/{user_id}/{pack_name}/`
4. Copy pack directory with all contents (metadata.yaml + documents)
5. Update pack metadata with import timestamp, imported_from: "marketplace"
6. Return import confirmation

**Error Handling:**
- Pack not found → 404
- Pack private → 403 Forbidden
- Pack already imported → 409 Conflict or just re-import
- Disk space issue → 507 Insufficient Storage
- Permission denied → 403

### Step 2: Backend Service Layer (60 min)

**File:** `deeptutor/services/knowledge/pack_manager.py`

Add method:
```python
async def import_pack(
    self,
    pack_name: str,
    user_id: str,
    source: str = "marketplace",
) -> PackMetadata:
    """Copy pack from marketplace to user workspace."""
    # 1. Get marketplace pack path
    # 2. Validate permissions
    # 3. Create destination directory
    # 4. Copy all files (shutil.copytree)
    # 5. Update metadata with import info
    # 6. Register pack in user's knowledge base index
    # 7. Return updated metadata
```

**Details:**
- Source: Get from marketplace directory or cache
- Destination: `data/knowledge_bases/{user_id}/{pack_name}`
- Copy with `shutil.copytree(src, dst, dirs_exist_ok=False)` to prevent overwrite
- Update metadata JSON with: `imported_from: "marketplace"`, `import_date: now()`
- Return PackMetadata object

### Step 3: Frontend API Client (30 min)

**File:** `web/lib/marketplace-api.ts`

Add function:
```typescript
export async function importMarketplacePack(
  packName: string,
): Promise<{ success: boolean; pack: MarketplacePack }> {
  const response = await fetch(
    apiUrl(`/api/v1/marketplace/import/${packName}`),
    { method: "POST" }
  );
  if (!response.ok) {
    throw new Error(`Failed to import: ${response.statusText}`);
  }
  return response.json();
}
```

**Details:**
- POST to `/api/v1/marketplace/import/{pack_name}`
- Handle errors: throw readable error messages
- Return imported pack data or null on failure
- No request body needed (pack name in URL)

### Step 4: Frontend Component (30 min)

**File:** `web/app/(utility)/marketplace/page.tsx`

Replace `handleImportPack` function:
```typescript
const handleImportPack = async (packName: string) => {
  setImporting(packName);
  try {
    const result = await importMarketplacePack(packName);
    setImportSuccess(packName);
    setTimeout(() => setImportSuccess(null), 3000);
    
    // Refresh pack list to show import status
    loadPacks();
  } catch (err) {
    setError(
      err instanceof Error ? err.message : "Failed to import pack"
    );
  } finally {
    setImporting(null);
  }
};
```

**Details:**
- Call real API endpoint instead of fake delay
- Handle response/errors appropriately
- Refresh marketplace list after successful import (shows updated session count)
- Show error message if import fails
- Keep loading state visual during import

---

## Testing Checklist

### Manual Testing (Local)
- [ ] Start backend and frontend locally
- [ ] Navigate to marketplace
- [ ] Click import button on any pack
- [ ] See loading indicator while importing
- [ ] See success message on completion
- [ ] Navigate to Knowledge Pack list
- [ ] Verify imported pack appears in list
- [ ] Verify pack documents are accessible
- [ ] Try importing same pack again (should handle gracefully)
- [ ] Test error cases:
  - [ ] Simulate API error → see error message
  - [ ] Try importing while offline → see error
  - [ ] Import pack with special characters → verify handling

### Integration Testing (if time permits)
- [ ] Verify imported pack can be used in assessment generation
- [ ] Check import metadata is correctly recorded
- [ ] Verify import count increments on marketplace (optional)

---

## Dependencies & Prerequisites

**Backend:**
- Marketplace pack directory structure exists and is readable
- Knowledge base manager can write to user workspace directory
- User session/authentication available in request context

**Frontend:**
- Marketplace API client library (marketplace-api.ts) exists
- API base URL correctly configured

**No Blockers:** All dependencies satisfied in current codebase

---

## Architecture Changes

**New Endpoint:**
```
POST /api/v1/marketplace/import/{pack_name}
├── Validate pack exists & is shareable
├── Copy to user workspace
└── Return imported pack metadata
```

**File Flow:**
```
marketplace/{pack_name}/
├── metadata.yaml
├── documents/
│   └── *.pdf
└── assessments/
    └── config.yaml

Copy to:
knowledge_bases/{user_id}/{pack_name}/
├── metadata.yaml (+ imported_from, import_date)
├── documents/
└── assessments/
```

**No database schema changes** - use existing pack metadata structure

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Import fails silently | High | Poor UX | Add detailed error messages |
| Pack already exists | Medium | Conflict | Handle with 409 or overwrite option |
| Disk space issue | Low | Failure | Add disk check, return 507 |
| Slow copy performance | Low | UX lag | Show progress indicator |

---

## Success Criteria

✅ **Definition of Done:**
1. API endpoint created and tested locally
2. Import actually copies pack files to workspace
3. Frontend calls real endpoint instead of fake
4. Error handling shows user-friendly messages
5. Imported pack accessible in Knowledge Pack list
6. PR includes architecture note with Mermaid diagram
7. Daily log updated with completion status

---

## Effort Estimate

| Component | Time | Est. |
|-----------|------|------|
| Backend API endpoint | 90 min | ✓ |
| Backend service layer | 60 min | ✓ |
| Frontend API client | 30 min | ✓ |
| Frontend component update | 30 min | ✓ |
| Testing & validation | 20 min | ✓ |
| **Total** | **230 min** | **~4 hours** |

---

## Next Steps

1. ✅ Read and approve this task packet
2. → Implement backend API endpoint (Step 1)
3. → Implement backend service (Step 2)
4. → Implement frontend client (Step 3)
5. → Update frontend component (Step 4)
6. → Manual testing
7. → Create PR with architecture note
8. → Update `ai_first/TASK_REGISTRY.json` status → "completed"
9. → Start T010 (Assessment Feedback Analysis)

---

## Reference Files

- **Audit Report:** `ai_first/MVP_GAP_ANALYSIS.md` (lines describing T009)
- **Task Registry:** `ai_first/TASK_REGISTRY.json` (T009 object)
- **Current Implementation:** `web/app/(utility)/marketplace/page.tsx` (lines 60-75)
- **API File:** `deeptutor/api/routers/marketplace.py`
- **API Client:** `web/lib/marketplace-api.ts`

---

**Created:** 2026-04-20  
**Status:** Ready for Implementation  
**Assigned Pod:** pod-a/marketplace-pack-import
