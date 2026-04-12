# Main System Map

Last updated: 2026-04-12

This is the required top-level Mermaid map for the project. Any PR that adds, removes, or materially changes product features, capabilities, tools, routers, routes, data models, or AI-first workflow must update this map.

```mermaid
flowchart TD
  Project["Multiagent Learning Platform"]

  Project --> Entry["Entry Points"]
  Entry --> Web["Next.js Web App"]
  Entry --> API["FastAPI API"]
  Entry --> CLI["Typer CLI"]
  Entry --> SDK["Python SDK"]

  Project --> Runtime["Agent-native Runtime"]
  Runtime --> Orchestrator["ChatOrchestrator"]
  Runtime --> ToolRegistry["ToolRegistry"]
  Runtime --> CapabilityRegistry["CapabilityRegistry"]
  Runtime --> StreamBus["StreamBus"]

  ToolRegistry --> Tools["Built-in Tools"]
  Tools --> RagTool["rag"]
  Tools --> WebSearch["web_search"]
  Tools --> CodeExecution["code_execution"]
  Tools --> Reason["reason"]
  Tools --> Brainstorm["brainstorm"]

  CapabilityRegistry --> Capabilities["Capabilities"]
  Capabilities --> Chat["chat"]
  Capabilities --> DeepSolve["deep_solve"]
  Capabilities --> DeepQuestion["deep_question"]

  Project --> Product["Contest MVP Product Layer"]
  Product --> TeacherWorkspace["Teacher Workspace"]
  Product --> KnowledgePack["Knowledge Pack"]
  Product --> AssessmentBuilder["Assessment Builder"]
  Product --> StudentTutor["Student Tutor Workspace"]
  Product --> TeacherDashboard["Teacher Dashboard"]

  Project --> Data["Data Layer"]
  Data --> SQLite["data/user/chat_history.db"]
  Data --> KnowledgeBases["data/knowledge_bases"]
  Data --> Memory["data/memory"]
  Data --> Settings["data/user/settings"]
  Data --> Workspace["data/user/workspace"]

  Project --> AIFirst["AI-first Operating Layer"]
  AIFirst --> OperatingPrompt["ai_first/AI_OPERATING_PROMPT.md"]
  AIFirst --> CurrentState["ai_first/CURRENT_STATE.md"]
  AIFirst --> NextActions["ai_first/NEXT_ACTIONS.md"]
  AIFirst --> Specs["docs/superpowers/specs"]
  AIFirst --> Plans["docs/superpowers/plans"]
  AIFirst --> Tasks["docs/superpowers/tasks"]
  AIFirst --> PRNotes["docs/superpowers/pr-notes"]
  AIFirst --> Evidence["ai_first/evidence"]
```
