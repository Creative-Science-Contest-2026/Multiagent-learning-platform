# Task Packet: T011 KB Context Badges

Date: 2026-04-20  
Branch: pod-a/marketplace-pack-import  
Priority: Critical (P3)

## Goal

Display active knowledge base context during tutoring so users know which sources are grounding each exchange.

## Scope

- Frontend chat rendering:
  - `web/components/chat/home/ChatMessages.tsx`
- Show KB badges from request snapshot in both:
  - user message bubble
  - paired assistant response block

## Acceptance Criteria

- If a request contains `knowledgeBases`, the chat UI shows KB chips.
- Chips appear for user messages and nearby assistant messages.
- No rendering change for messages without KB context.
- Existing message actions/retry flow stay intact.

## Validation

- Frontend lint passes for modified chat component.
- Manual UI check in workspace chat route.
