# C216 Contest Shell Scope Trim Design

## Goal

Make the contest shell read as one bounded classroom product by visually prioritizing the contest loop routes and demoting inherited DeepTutor utility routes without removing route access.

## Current behavior

- `SidebarShell.tsx` renders one flat `PRIMARY_NAV` list where `Chat`, `TutorBot`, `Co-Writer`, `Guided Learning`, `Dashboard`, `Knowledge`, `Marketplace`, and `Memory` appear as peers.
- The shell header and route ordering make inherited tooling feel equal to the contest loop, even though the contest story depends mostly on `Knowledge`, `/agents`, and `Dashboard`.
- `WorkspaceSidebar.tsx` and `UtilitySidebar.tsx` only pass session behavior into the shared shell; they do not currently influence information architecture.

## Intended behavior

- The expanded shell should present a clear contest-core group first and a secondary-tools group after it.
- The collapsed shell should keep only the core routes visible by default, while secondary tools remain reachable via the expanded shell.
- Route implementations, navigation targets, session handling, and copy keys stay unchanged.

## Candidate approaches

### Approach 1: Reorder the existing flat list only

- Pros: smallest patch.
- Cons: inherited tools still look primary because there is no visual separation.

### Approach 2: Split the shell into explicit contest-core and secondary tool groups

- Pros: clearest first impression, preserves all routes, fits the task packet boundary.
- Cons: requires modest sidebar structure changes in expanded and collapsed modes.

## Chosen approach

Use **Approach 2**. Keep one shared nav definition in `SidebarShell.tsx`, but classify entries into:

- contest core: `Knowledge`, `Dashboard`, `/agents`, and `Marketplace`
- secondary tools: `Chat`, `Guided Learning`, `Co-Writer`, and `Memory`

The expanded shell will render grouped sections. The collapsed shell will render the core routes and continue to expose the `/agents` recent-tutor affordance.

## Files expected to change

- `web/components/sidebar/SidebarShell.tsx`
- `web/components/sidebar/WorkspaceSidebar.tsx` only if prop naming or defaults must be clarified
- `web/components/sidebar/UtilitySidebar.tsx` only if prop naming or defaults must be clarified
- `web/app/(workspace)/layout.tsx` only if shell spacing needs a tiny companion adjustment
- `web/app/(utility)/layout.tsx` only if shell spacing needs a tiny companion adjustment

## Files reviewed but expected unchanged

- `web/app/(workspace)/page.tsx`
- `web/app/(workspace)/dashboard/page.tsx`
- `web/app/(workspace)/agents/page.tsx`
- `web/app/(utility)/knowledge/page.tsx`
- all backend and API modules

## Tests to add or update

- Add a focused component test for `SidebarShell` that verifies grouped core-vs-secondary rendering in expanded mode.
- Add a focused component test for `SidebarShell` collapsed mode that verifies secondary tools are not shown there.
- Run targeted frontend test command plus the existing lint/build checks from the task packet.
