# Code Review Graph Integration Design

- Date: 2026-04-30
- Task ID: `OPS_CODE_REVIEW_GRAPH_INTEGRATION`
- Branch: `fix/code-review-graph-integration`

## Goal

Add `code-review-graph` to this repository in a way that Codex can use immediately, the repo carries its own integration files, and the first graph snapshot is committed if the tool stores it inside the project.

## Current Behavior

- This repository already has AI-first operating instructions, but no `code-review-graph` integration.
- There is no project-local `code-review-graph` artifact or generated `.claude/skills` content.
- There is no committed `.code-review-graph/` graph artifact in the repository.
- The machine can install developer tooling globally, but repo-local integration still needs to be written inside this project.

## Intended Behavior Change

- `code-review-graph` should be installed and available on this machine.
- This repository should be configured for Codex via the tool's Codex installation path.
- The initial graph build should run in this repository.
- Any repo-local configuration or graph artifact produced by the tool, including `.gitignore`, `.claude/skills/`, and `.code-review-graph/` if created, should be committed on this lane.

## Codebase Survey

### Entry points and handlers

- `.gitignore`
  - the upstream install flow appends ignore rules for graph artifacts
- `.claude/skills/`
  - the upstream install flow generates repo-local skill markdown files

### Primary service or use-case modules

- no product runtime module is being extended
- the integration is primarily repo tooling plus generated graph metadata

### Shared contracts, schemas, or types

- `~/.codex/config.toml`
  - global Codex MCP registration point that the upstream install flow updates for the current machine

### Adjacent or reused flows inspected

- `~/.codex/AGENTS.md` and `~/.codex/RTK.md` are already configured globally for RTK
- this lane should not replace or remove the existing global RTK guidance
- the actual upstream Codex flow writes the MCP server entry to `~/.codex/config.toml`, appends `.code-review-graph/` to repo `.gitignore`, and generates `.claude/skills/*.md` inside the project rather than patching `AGENTS.md`

### Closest existing tests

- no existing automated test covers tooling integration for Codex instructions
- validation will rely on the upstream CLI commands, generated file inspection, and `git diff --check`

## Candidate Approaches

### Approach A: Global-only installation, no repo integration

- Install `code-review-graph` on the machine and stop there.
- Pros:
  - smallest repo diff
  - avoids project-level instruction changes
- Cons:
  - does not satisfy the request to integrate it into this repository
  - future contributors would not inherit repo-local setup

### Approach B: Global tool install plus repo-local Codex integration and initial build

- Install the CLI on the machine, then run `code-review-graph install --platform codex` and `code-review-graph build` inside this worktree, committing the generated repo-local files.
- Pros:
  - matches the upstream quick start
  - keeps the Python package out of tracked repo dependencies
  - gives the repo a committed initial graph snapshot if the tool creates one locally
- Cons:
  - may patch `AGENTS.md` and add generated files that need review

### Approach C: Vendor the upstream project into this repository

- Add the entire `code-review-graph` source tree as an internal dependency or subdirectory.
- Pros:
  - fully self-contained
- Cons:
  - far broader than needed
  - high review and maintenance cost
  - not what the upstream README recommends

## Chosen Approach

Approach B.

It satisfies the user's request while keeping the repository dependency surface bounded. The machine-level install provides the executable, and the repo-local `install` plus `build` steps create the actual project integration that future Codex sessions can use.

## Planned Changes

- Install `code-review-graph` on the machine with a non-repo dependency path.
- Run `code-review-graph install --platform codex` in this repository.
- Review and keep the generated modifications in:
  - `.gitignore`
  - `.claude/skills/`
  - `.code-review-graph/` if present
- Add a PR architecture note describing the tooling integration lane and generated graph artifact.

## Expected Impact Surface

### Likely to change

- `.gitignore`
- `.claude/skills/`
- `.code-review-graph/`

### Reviewed but expected to remain unchanged

- application/runtime source files under `deeptutor/`, `deeptutor_cli/`, and `web/`
- lockfiles and package manifests unless the chosen installation path unexpectedly requires a tracked repo dependency change

## Tests To Run

- `~/Library/Python/3.12/bin/code-review-graph install --platform codex`
- `~/Library/Python/3.12/bin/code-review-graph build`
- `~/Library/Python/3.12/bin/code-review-graph status`
- `git diff --check`

## Non-Goals

- no product feature changes
- no backend/runtime code changes
- no migration of existing RTK global integration
