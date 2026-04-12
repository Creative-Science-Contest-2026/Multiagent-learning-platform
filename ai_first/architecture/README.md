# Architecture Maps

This folder stores Mermaid diagrams that keep the AI-first project understandable as multiple AI agents make changes.

## Main map

`MAIN_SYSTEM_MAP.md` is the top-level system map. Update it when a PR adds, removes, or materially changes:

- capabilities;
- tools;
- API routers;
- major frontend routes;
- data models or storage locations;
- Teacher -> Student -> Dashboard flows;
- AI-first workflow rules.

## Feature maps

Feature-specific diagrams live in `feature-maps/`.

Every PR must include a PR architecture note under `docs/superpowers/pr-notes/` with at least one Mermaid diagram.
