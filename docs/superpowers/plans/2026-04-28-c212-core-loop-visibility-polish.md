# C212 Core Loop Visibility Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, reusable contest-loop visibility strip to the key Knowledge, Assessment, Tutor, and Dashboard screens so the five-step submission story is visible in-product.

**Architecture:** Build one shared React component for the loop strip, then place it in the four scoped screens using screen-specific current-step and helper text props. Keep styling consistent with existing card headers and avoid any routing, data, or backend changes.

**Tech Stack:** Next.js App Router, React 19, TypeScript, Tailwind utility classes, lucide-react, existing `react-i18next` usage.

---

## File Structure

- Create: `web/components/contest/CoreLoopVisibilityStrip.tsx`
  Responsibility: render the five-step contest loop with current-step and next-step emphasis.
- Modify: `web/app/(utility)/knowledge/page.tsx`
  Responsibility: show the loop at the source-knowledge stage.
- Modify: `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`
  Responsibility: show the loop at the assessment stage.
- Modify: `web/app/(workspace)/agents/[botId]/chat/page.tsx`
  Responsibility: show the loop at the tutor stage in a compact layout.
- Modify: `web/app/(workspace)/dashboard/page.tsx`
  Responsibility: show the loop at the diagnosis stage and frame intervention as the next move.

## Task 1: Create the shared visibility strip

**Files:**
- Create: `web/components/contest/CoreLoopVisibilityStrip.tsx`

- [ ] Define a fixed ordered step list with the labels `Knowledge Pack`, `Assessment`, `Tutor`, `Diagnosis`, and `Intervention`.
- [ ] Implement typed props for `currentStep`, optional `nextStep`, optional `compact`, and optional `helperText`.
- [ ] Render a label, helper text, and step pills with three visual states: active, next, and inactive.
- [ ] Keep the component wrapping cleanly on mobile by using flex-wrap and compact text sizing.

## Task 2: Add the strip to Knowledge

**Files:**
- Modify: `web/app/(utility)/knowledge/page.tsx`

- [ ] Import the shared strip.
- [ ] Add the strip to the page header area with `currentStep="Knowledge Pack"` and `nextStep="Assessment"`.
- [ ] Use helper text that frames the page as the teacher-owned source material stage.

## Task 3: Add the strip to Assessment review

**Files:**
- Modify: `web/app/(workspace)/dashboard/assessments/[sessionId]/page.tsx`

- [ ] Import the shared strip.
- [ ] Insert it below the main header and above the existing three summary cards.
- [ ] Set `currentStep="Assessment"` and `nextStep="Tutor"` with helper text that preserves the teacher review safety framing.

## Task 4: Add the strip to Tutor chat

**Files:**
- Modify: `web/app/(workspace)/agents/[botId]/chat/page.tsx`

- [ ] Import the shared strip.
- [ ] Place it below the slim chat header and above the message list.
- [ ] Use `compact` mode with `currentStep="Tutor"` and `nextStep="Diagnosis"` so the chat screen keeps its minimal density.

## Task 5: Add the strip to Dashboard

**Files:**
- Modify: `web/app/(workspace)/dashboard/page.tsx`

- [ ] Import the shared strip.
- [ ] Place it inside the hero card above the existing workflow summary blocks.
- [ ] Set `currentStep="Diagnosis"` and `nextStep="Intervention"` with helper text that keeps the dashboard framed as a teacher action surface.

## Task 6: Validation and PR metadata

**Files:**
- Modify: `ai_first/ACTIVE_ASSIGNMENTS.md`
- Modify: `ai_first/TASK_REGISTRY.json`
- Modify: `ai_first/daily/2026-04-28.md`
- Create: `docs/superpowers/pr-notes/2026-04-28-c212-core-loop-visibility-polish.md`

- [ ] Mark Session C active for `C212`.
- [ ] Move `C212_CORE_LOOP_VISIBILITY_POLISH` to `in-progress`.
- [ ] Record the implementation and validation commands in the daily log.
- [ ] Add the required PR note with a Mermaid diagram and state that `MAIN_SYSTEM_MAP.md` was not updated.

## Validation

- [ ] Run: `cd web && npx eslint app/'(utility)'/knowledge/page.tsx app/'(workspace)'/dashboard/page.tsx app/'(workspace)'/dashboard/assessments/[sessionId]/page.tsx app/'(workspace)'/agents/[botId]/chat/page.tsx components/contest/*.tsx`
- [ ] Run: `cd web && npm run build`
- [ ] Run: `git diff --check`
