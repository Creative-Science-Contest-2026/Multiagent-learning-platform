# Knowledge Pack Wizard Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the `Gói kiến thức` page into a Vietnamese-first three-step wizard with a right-side ingestion status panel, no FE notebook branch, and no user-facing model/provider selector.

**Architecture:** Keep the route the same but split the current monolithic screen into a small set of focused FE sections: wizard state, ingestion/status panel, and simplified pack cards. Route all creation/indexing through a default backend OpenAI indexing path, and extend the data contract only where needed to render overall and per-file status in step `Hoàn tất`.

**Tech Stack:** Next.js App Router, React state/hooks, existing web locale JSON files, existing knowledge-pack API flow, Python backend knowledge-pack/indexing services

---

### Task 1: Audit The Existing Knowledge-Pack Data Contract

**Files:**
- Review: `web/app/(utility)/knowledge/page.tsx`
- Review: backend knowledge-pack and indexing handlers reachable from the current create/upload flow
- Review: any FE API wrappers used by the knowledge page

- [ ] **Step 1: Trace the FE create/upload calls to the exact backend endpoints**

```bash
rg -n "createKnowledgeBase|uploadToKnowledgeBase|setSelectedProvider|providers|progress" web/app/'(utility)'/knowledge/page.tsx web/lib deeptutor/api deeptutor/services -S
```

- [ ] **Step 2: Record the contract gaps that block the target wizard**

Run: inspect the matched FE and backend files from Step 1
Expected: a written list of whether the backend already returns:
- overall knowledge-pack indexing status
- per-file upload/index status
- the current field name and persistence behavior for `Grade`
- where provider/model defaults are currently chosen

- [ ] **Step 3: Commit the contract/audit checkpoint**

```bash
git add docs/superpowers/plans/2026-04-30-knowledge-pack-wizard-redesign.md
git commit -m "docs(knowledge): record wizard redesign plan checkpoint [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```

### Task 2: Add Or Adjust Data Tests For The New Metadata And Status Contract

**Files:**
- Modify or create: backend tests that cover knowledge-pack create/upload/status behavior
- Modify or create: FE/unit tests for field mapping and completion-state rendering

- [ ] **Step 1: Write the failing backend-focused test for default indexing path**

```text
Test that a normal knowledge-pack create/upload flow does not require a user-provided provider/model choice and resolves to the default OpenAI indexing path.
```

- [ ] **Step 2: Run the focused backend test to verify the current behavior fails or is missing**

Run: the narrowest backend test command for the touched module, for example `pytest <exact-test-file> -k knowledge_pack -v`
Expected: FAIL or missing-coverage confirmation that proves the contract still needs implementation.

- [ ] **Step 3: Write the failing FE test for the new wizard labels and hidden notebook/provider controls**

```text
Add a focused test that asserts:
- no `Notebooks` tab on the knowledge page
- no provider/model selector
- `Mức độ khó` segmented control renders instead of the old `Grade` input
```

- [ ] **Step 4: Run the focused FE test to verify it fails**

Run: the narrowest FE test command for the new test file
Expected: FAIL because the current page still shows the old layout and controls.

- [ ] **Step 5: Commit the failing-test checkpoint**

```bash
git add <backend-test-files> <frontend-test-files>
git commit -m "test(knowledge): lock wizard redesign expectations [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```

### Task 3: Refactor The Knowledge Page Shell Into Wizard-Friendly FE Units

**Files:**
- Modify: `web/app/(utility)/knowledge/page.tsx`
- Create: extracted FE sections/components for:
  - wizard steps
  - status panel
  - simplified pack cards
- Modify: any FE helper/state files created to keep page logic bounded

- [ ] **Step 1: Extract the current notebook branch out of the visible page flow**

```text
Remove the page-level `Knowledge Packs / Notebooks` tab switcher from the visible screen and keep only the knowledge-pack branch active on this route.
```

- [ ] **Step 2: Replace the top create/upload cards with wizard state**

```text
Introduce explicit wizard steps:
- `Thông tin`
- `Tài liệu`
- `Hoàn tất`
with step navigation state stored in the page or a dedicated hook.
```

- [ ] **Step 3: Replace the old `Grade` field with a segmented `Mức độ khó` control**

```text
Implement three options:
- `Cơ bản`
- `Trung bình`
- `Nâng cao`
and map them through the FE state that currently backs the `Grade` metadata.
```

- [ ] **Step 4: Remove the provider/model selector from the create flow**

```text
Delete the visible selector from the wizard UI and remove any FE dependency on the user choosing a provider.
```

- [ ] **Step 5: Build the right-side status panel**

```text
Show active pack metadata and ingestion progress:
- tên gói
- chủ đề
- mức độ khó
- chương trình học
- số tài liệu
- trạng thái index
```

- [ ] **Step 6: Run the FE test and lint commands for the refactored page**

Run: focused FE tests plus targeted eslint on the touched files
Expected: PASS for the new wizard/notebook/provider visibility rules.

- [ ] **Step 7: Commit the FE shell refactor**

```bash
git add web/app/'(utility)'/knowledge/page.tsx web/components web/lib <new-test-files>
git commit -m "feat(knowledge): add wizard-first knowledge page shell [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```

### Task 4: Implement The File-Only Upload Step And Completion-State Rendering

**Files:**
- Modify: wizard step components and upload state handling
- Modify: FE API wrappers if needed
- Modify: backend progress/status endpoints if current data is insufficient

- [ ] **Step 1: Limit the document step to file upload only**

```text
Keep one dropzone-style file upload surface, remove notebook/link/provider branches, and render selected-file chips or rows before upload starts.
```

- [ ] **Step 2: Render step `Hoàn tất` with two levels of status**

```text
Top summary:
- uploaded count
- indexed count
- overall state

Bottom list:
- per-file name
- per-file status
- per-file error if present
```

- [ ] **Step 3: Extend backend or FE normalization if per-file state is missing**

```text
If the current API only returns aggregate KB progress, add the minimal contract needed so FE can render file-level status instead of inventing fake client-side states.
```

- [ ] **Step 4: Run focused backend and FE tests for upload/completion behavior**

Run:
- focused backend test command for create/upload/progress
- focused FE test command for completion-step rendering
Expected: PASS for overall and file-level status behavior.

- [ ] **Step 5: Commit the ingestion/status implementation**

```bash
git add web deeptutor <tests>
git commit -m "feat(knowledge): show file-level ingestion status [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```

### Task 5: Simplify Existing Pack Cards And Finish Vietnamese Copy Coverage

**Files:**
- Modify: existing pack list rendering in `web/app/(utility)/knowledge/page.tsx` or extracted card component
- Modify: `web/locales/vi/app.json`
- Modify: `web/locales/en/app.json`
- Modify: any FE tests that validate visible copy

- [ ] **Step 1: Reduce each pack card to the approved information set**

```text
Keep only:
- tên gói
- chủ đề
- mức độ khó
- chương trình học
- số tài liệu
- trạng thái index
```

- [ ] **Step 2: Reduce the default inline actions to the approved action set**

```text
Main actions:
- `Xem chi tiết`
- `Chỉnh sửa`

Secondary action:
- `Xóa`
```

- [ ] **Step 3: Complete the Vietnamese-first locale pass**

```text
Replace remaining visible English copy on this route, keeping technical English only where the system status genuinely needs it.
```

- [ ] **Step 4: Run locale and screen-level regression checks**

Run:
- the focused FE test for Vietnamese labels
- any existing locale JSON validity checks
- targeted eslint/build command for the touched screen
Expected: PASS with no newly introduced untranslated labels on the route.

- [ ] **Step 5: Commit the card and locale polish**

```bash
git add web/locales web/app/'(utility)'/knowledge/page.tsx web/components <tests>
git commit -m "feat(knowledge): simplify cards and localize wizard UI [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```

### Task 6: Final Verification, Docs, And Handoff

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-knowledge-pack-wizard-redesign.md`
- Update if required: `ai_first/architecture/MAIN_SYSTEM_MAP.md`

- [ ] **Step 1: Write the PR note with a Mermaid diagram**

```text
Document:
- wizard layout
- default OpenAI indexing path
- FE notebook/provider removal
- status panel and completion-state behavior
```

- [ ] **Step 2: Update the daily log with implementation and verification outcomes**

```text
Record what changed, what stayed out of scope, and the exact commands used for FE/backend verification.
```

- [ ] **Step 3: Decide whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` needs an update**

Run: inspect whether the final implementation changes product workflow or architecture enough to update the map
Expected: update the map only if the runtime/user-flow change materially changes the documented system structure.

- [ ] **Step 4: Run final verification**

Run:
- focused backend tests
- focused FE tests
- targeted eslint/build
- `git diff --check`
Expected: all relevant checks pass and the patch is formatting-clean.

- [ ] **Step 5: Commit the final docs/handoff checkpoint**

```bash
git add ai_first/daily/2026-04-30.md docs/superpowers/pr-notes/2026-04-30-knowledge-pack-wizard-redesign.md ai_first/architecture/MAIN_SYSTEM_MAP.md
git commit -m "docs(knowledge): capture wizard redesign handoff [UI_KNOWLEDGE_PACK_WIZARD_REDESIGN]"
```
