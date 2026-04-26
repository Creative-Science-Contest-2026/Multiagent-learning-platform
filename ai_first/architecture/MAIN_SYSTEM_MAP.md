# Main System Map

Last updated: 2026-04-26

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
  KnowledgePack --> KPVersions["Versioned teacher-pack metadata: current_version + version_history"]
  
  Product --> Marketplace["Knowledge Pack Marketplace"]
  Marketplace --> MarketplaceAPI["/api/v1/marketplace"]
  Marketplace --> MarketplaceUI["/marketplace"]
  Marketplace --> MarketplaceFilters["Search/Subject/Owner Filters"]
  Marketplace --> MarketplacePreview["GET /api/v1/marketplace/{pack_name}/preview"]
  MarketplacePreview --> PreviewModal["Preview modal: metadata + sample documents"]
  MarketplacePreview --> PackRatings["Average rating + recent reviews"]
  Marketplace --> MarketplaceImport["POST /api/v1/marketplace/import/{pack_name}"]
  Marketplace --> MarketplaceBatchImport["POST /api/v1/marketplace/import-batch"]
  Marketplace --> MarketplaceReviewAPI["POST /api/v1/marketplace/{pack_name}/reviews"]
  MarketplaceReviewAPI --> ReviewStorage["KB config: marketplace_reviews metadata"]
  MarketplaceImport --> ImportedClone["Imported KB clone: <pack>__imported"]
  MarketplaceBatchImport --> BatchSelectUI["Multi-select cards + import selected action bar"]
  MarketplaceBatchImport --> ImportedClone
  ImportedClone --> OfflinePackManifest["Browser offline imported-pack manifest"]
  
  Product --> AssessmentBuilder["Assessment Builder"]
  AssessmentBuilder --> QuizGrounding["Knowledge Pack Grounded Quiz Config"]
  AssessmentBuilder --> AdaptiveDifficulty["Adaptive Difficulty from Recent Quiz Performance"]
  AssessmentBuilder --> AssessmentRecommendAPI["POST /api/v1/assessment/recommend"]
  AssessmentBuilder --> AssessmentDiagnosisAPI["GET /api/v1/assessment/diagnosis/{session_id}"]
  AssessmentRecommendAPI --> RecommendEngine["Assessment Recommendation Engine"]
  RecommendEngine --> AssessmentSignals["Weak topics + score trend + KB context"]
  AssessmentDiagnosisAPI --> EvidenceExtractor["Observation extractor from quiz review"]
  EvidenceExtractor --> ObservationStore["SQLite observations + student_states"]
  ObservationStore --> DiagnosisEngine["Rule-first diagnosis + action selection"]
  AdaptiveDifficulty --> QuizHistory["[Quiz Performance] session context"]
  AdaptiveDifficulty --> DeepQuestion
  
  Product --> StudentTutor["Student Tutor Workspace"]
  StudentTutor --> TutorKBContext["Knowledge Pack Tutoring Context"]
  StudentTutor --> TutorKBBadges["KB Context Badges in Chat Messages"]
  StudentTutor --> TutorFollowups["Optional follow-up questions in tutor replies"]
  TutorKBBadges --> SnapshotKBs["Message requestSnapshot.knowledgeBases"]
  TutorFollowups --> ChatResponse["Agentic chat final response section: Follow-up questions"]
  
  Product --> TeacherDashboard["Teacher Dashboard"]
  TeacherDashboard --> DashboardSummary["Session Activity Summary"]
  DashboardSummary --> DashboardFilters["History filters: type + KB + search + min score"]
  DashboardSummary --> TeacherAnalytics["Teacher Analytics Signals"]
  TeacherDashboard --> TeacherInsights["Teacher Insight Panel"]
  TeacherAnalytics --> EngagementSignals["Engagement: active days + streak + KB usage"]
  TeacherAnalytics --> AssessmentTrend["Assessment trend: average + latest + delta"]
  TeacherAnalytics --> DifficultySignals["Learning signals: focus topics + strong areas"]
  TeacherInsights --> InsightsAPI["GET /api/v1/dashboard/insights"]
  InsightsAPI --> DiagnosisEngine
  InsightsAPI --> SmallGroupRecommendations["Small-group recommendation clusters"]
  TeacherDashboard --> StudentDashboard["Student Progress Dashboard"]
  TeacherDashboard --> AssessmentReview["Assessment Review Drill-down"]
  StudentDashboard --> StudentRoute["/dashboard/student"]
  StudentDashboard --> StudentProgressAPI["GET /api/v1/dashboard/student-progress"]
  StudentDashboard --> TrendCards["Streak + average score + recent assessments"]
  StudentDashboard --> TopicSignals["Focus topics + mastered topics"]
  StudentDashboard --> LearningPathSignals["Suggested learning path sequence"]
  LearningPathSignals --> PathEngine["Deterministic learning-path helper"]
  PathEngine --> FocusTopicInputs["Focus topics from assessment analysis"]
  PathEngine --> ObjectiveInputs["Knowledge-pack learning_objectives metadata"]
  AssessmentReview --> ReviewRoute["/dashboard/assessments/[sessionId]"]
  AssessmentReview --> ReviewAPI["/api/v1/sessions/{session_id}/assessment-review"]
  AssessmentReview --> OfflineQuizQueue["Browser offline quiz-result sync queue"]
  AssessmentReview --> ProgressIndicator["ProgressIndicator Component"]
  AssessmentReview --> LearningJourney["LearningJourneySummary Component"]
  AssessmentReview --> TimeMetrics["Timing metrics: total + average + per-question response time"]
  AssessmentReview --> AssessErrorBoundary["Route Error Boundary: /dashboard/assessments/error.tsx"]
  ReviewAPI --> QuizTranscript["[Quiz Performance] transcript with optional time: Ns suffix"]
  ProgressIndicator --> ScoreViz["Score Progress Bar + Recommendations"]
  LearningJourney --> TopicBadges["Mastered/Recommended Topics"]
  Marketplace --> MarketErrorBoundary["Route Error Boundary: /marketplace/error.tsx"]

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
  API --> APISecurity["API Security Middleware"]
  APISecurity --> RateLimit["Rate limiting + 429 Retry-After"]
  MergeGates --> PRs
  MergeGates --> CI
  MergeGates --> Reviews
  NextTask --> Issues
  NextTask --> Tasks
  NextTask --> NextActions
```
