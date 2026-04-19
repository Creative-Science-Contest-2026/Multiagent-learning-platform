# Main System Map

Last updated: 2026-04-20

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
  KnowledgePack --> KPMetaFlow["Metadata Create/Edit/Update Flow"]
  
  Product --> Marketplace["Knowledge Pack Marketplace"]
  Marketplace --> MarketplaceAPI["/api/v1/marketplace"]
  Marketplace --> MarketplaceUI["/marketplace"]
  Marketplace --> MarketplaceFilters["Search/Subject/Owner Filters"]
  
  Product --> AssessmentBuilder["Assessment Builder"]
  AssessmentBuilder --> QuizGrounding["Knowledge Pack Grounded Quiz Config"]
  
  Product --> StudentTutor["Student Tutor Workspace"]
  StudentTutor --> TutorKBContext["Knowledge Pack Tutoring Context"]
  
  Product --> TeacherDashboard["Teacher Dashboard"]
  TeacherDashboard --> DashboardSummary["Session Activity Summary"]
  TeacherDashboard --> AssessmentReview["Assessment Review Drill-down"]
  AssessmentReview --> ReviewRoute["/dashboard/assessments/[sessionId]"]
  AssessmentReview --> ReviewAPI["/api/v1/sessions/{session_id}/assessment-review"]
  AssessmentReview --> ProgressIndicator["ProgressIndicator Component"]
  AssessmentReview --> LearningJourney["LearningJourneySummary Component"]
  ProgressIndicator --> ScoreViz["Score Progress Bar + Recommendations"]
  LearningJourney --> TopicBadges["Mastered/Recommended Topics"]

  Project --> Localization["Internationalization (i18n)"]
  Localization --> UITranslations["UI Translations"]
  UITranslations --> EnglishUI["web/locales/en/"]
  UITranslations --> ChineseUI["web/locales/zh/"]
  UITranslations --> VietnameseUI["web/locales/vi/"]
  Localization --> PromptSystem["Prompt Localization"]
  PromptSystem --> PromptManager["PromptManager (unified)"]
  PromptManager --> VietnameseFallback["vi → en fallback chain"]
  Localization --> LanguageSettings["Settings: en/zh/vi"]

  Project --> Data["Data Layer"]
  Data --> SQLite["data/user/chat_history.db"]
  Data --> KnowledgeBases["data/knowledge_bases"]
  Data --> Memory["data/memory"]
  Data --> Settings["data/user/settings"]
  Data --> Workspace["data/user/workspace"]

  Project --> AIFirst["AI-first Operating Layer"]
  AIFirst --> OperatingPrompt["ai_first/AI_OPERATING_PROMPT.md"]
  AIFirst --> Roadmap["ai_first/AI_FIRST_ROADMAP.md"]
  AIFirst --> CurrentState["ai_first/CURRENT_STATE.md"]
  AIFirst --> NextActions["ai_first/NEXT_ACTIONS.md"]
  AIFirst --> Specs["docs/superpowers/specs"]
  AIFirst --> Plans["docs/superpowers/plans"]
  AIFirst --> Tasks["docs/superpowers/tasks"]
  AIFirst --> Evidence["ai_first/evidence"]
  AIFirst --> AutoLoop["Autonomous completion loop"]
  AutoLoop --> MergeGates["Safe merge gates"]
  AutoLoop --> NextTask["Next task selection"]

  Project --> GitHub["GitHub Execution Layer"]
  GitHub --> Issues["Issues"]
  GitHub --> Labels["pod-a / pod-b / blocked / needs-review"]
  GitHub --> PRs["Pull Requests"]
  GitHub --> CI["CI Checks"]
  GitHub --> Reviews["Review blockers"]
  PRs --> PRNotes["docs/superpowers/pr-notes"]
  PRs --> CI
  PRs --> Reviews
  MergeGates --> PRs
  MergeGates --> CI
  MergeGates --> Reviews
  NextTask --> Issues
  NextTask --> Tasks
  NextTask --> NextActions
```
