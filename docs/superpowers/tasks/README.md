# Task Packets

Task packets are the execution contract for Feature Pods.

Each task packet must define:

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
3. Create or switch to the task branch.
4. Work only inside the packet's owned-file scope.

Use `ai_first/ACTIVE_ASSIGNMENTS.md` for short-lived active coordination and the task packet for the execution contract.
