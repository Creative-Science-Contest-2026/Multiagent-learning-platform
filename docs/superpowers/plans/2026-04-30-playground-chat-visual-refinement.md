# Playground Chat Visual Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Soften the `/playground` chat UI so traces remain visible but feel calmer, lighter, and more product-like.

**Architecture:** Keep the existing runtime structure and data surfaces, but restyle message bubbles, trace accordions, process logs, metadata cards, and the command bar into a subtler visual system. Avoid any backend or interaction-logic changes.

**Tech Stack:** Next.js App Router, React, TypeScript, Tailwind-style utility classes, ESLint

---

### Task 1: Refine shared supporting surfaces

**Files:**
- Modify: `web/components/common/AssistantResponse.tsx`
- Modify: `web/components/common/ProcessLogs.tsx`

- [ ] Soften `AssistantResponse` default presentation so markdown output reads like calm content rather than a hard card body.
- [ ] Make `ProcessLogs` default closed and restyle its shell, header, and log rows into a subtler collapsed annotation surface.
- [ ] Keep all data visible when expanded; only presentation and default-open behavior should change.

### Task 2: Refine trace and result surfaces inside `/playground`

**Files:**
- Modify: `web/app/(workspace)/playground/page.tsx`

- [ ] Soften `TracePanel` accordions so `Thinking`, `Acting`, `Observing`, and related rows default closed and use lighter borders/backgrounds.
- [ ] Restyle tool-call, tool-result, progress, and error sub-blocks to feel like supporting annotations instead of debug panels.
- [ ] Restyle `CapabilityResultPanel` response and metadata blocks so metadata defaults closed and reads as lower-priority supporting evidence.

### Task 3: Refine conversation bubbles and command bar

**Files:**
- Modify: `web/app/(workspace)/playground/page.tsx`
- Modify: `web/components/chat/home/PlaygroundRightPanel.tsx`

- [ ] Change user bubbles from dark charcoal to a lighter same-family tone with gentle contrast.
- [ ] Keep assistant cards slightly brighter and calmer, with softer shadow/border treatment.
- [ ] Lighten the bottom command-bar chrome and send/generate buttons so the composer feels quieter and more refined.
- [ ] If needed, slightly soften the right panel header chrome so it matches the calmer chat surface.

### Task 4: Verify and record handoff

**Files:**
- Modify: `ai_first/daily/2026-04-30.md`
- Create: `docs/superpowers/pr-notes/2026-04-30-playground-chat-visual-refinement.md`

- [ ] Run: `cd web && npx eslint "app/(workspace)/playground/page.tsx" "components/common/AssistantResponse.tsx" "components/common/ProcessLogs.tsx" "components/chat/home/PlaygroundRightPanel.tsx"`
- [ ] Run: `cd web && npm run build`
- [ ] Write the PR note with a Mermaid diagram and state whether `ai_first/architecture/MAIN_SYSTEM_MAP.md` changed.
