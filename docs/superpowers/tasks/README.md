# Task Packets

Task packets are the execution contract for Feature Pods.

Each task packet must define:

- task ID;
- commit tag;
- owner;
- branch;
- GitHub issue;
- goal;
- user-visible outcome;
- owned files/modules;
- do-not-touch files/modules;
- API/data contract;
- acceptance criteria;
- required tests;
- manual verification;
- handoff notes.

Mirror active task packets to GitHub Issues when two AI agents are working in parallel.

## Active assignment workflow

Before code work starts on a task:

1. Confirm the task packet is current.
2. Add the task to `ai_first/ACTIVE_ASSIGNMENTS.md`.
3. If another session is active on the same machine, create or switch to a separate worktree for this task.
4. Create or switch to the task branch inside that task's own worktree.
5. Run `git fetch origin main` and merge `origin/main` into the task branch when `main` has advanced before continuing feature edits.
6. Confirm the packet's `Task ID` and `Commit tag` before making the first commit.
7. Work only inside the packet's owned-file scope.

Use `ai_first/ACTIVE_ASSIGNMENTS.md` for short-lived active coordination and the task packet for the execution contract.
