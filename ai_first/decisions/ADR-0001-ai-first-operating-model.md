# ADR-0001: Hybrid AI-first Operating Model

Date: 2026-04-12

## Status

Accepted.

## Context

The project will be implemented by two humans and two AI agents running on two machines. The goal is to submit a reliable MVP to VnExpress Sáng kiến Khoa học 2026.

The team needs a process where AI can propose, implement, test, and document work while humans review product behavior and major decisions.

## Decision

Use a hybrid model:

- Repository Markdown stores long-term truth: specs, plans, tasks, architecture maps, prompts, evidence, and daily logs.
- GitHub Issues and Pull Requests coordinate active execution.
- Each AI works in a separate branch and owns clearly defined files/modules.
- Every PR includes a Markdown architecture note with Mermaid.
- Structural PRs update `ai_first/architecture/MAIN_SYSTEM_MAP.md`.

## Consequences

The project gains durable context for AI workers and a clear review trail for humans.

The cost is additional documentation discipline. This cost is accepted because two AI agents working in parallel need explicit contracts.
