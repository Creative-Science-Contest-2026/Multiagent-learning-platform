import { apiUrl } from "@/lib/api";

export interface AssessmentSummary {
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  score_percent: number;
  estimated_time_spent?: number;
  average_time_per_question?: number;
}

export interface AssessmentReviewResult {
  question_id: string;
  question: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  duration_seconds?: number | null;
}

export interface AssessmentReview {
  session_id: string;
  title: string;
  timestamp: number;
  status: string;
  knowledge_bases: string[];
  summary: AssessmentSummary;
  results: AssessmentReviewResult[];
}

export interface TopicPerformance {
  topic: string;
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  accuracy_percent: number;
}

export interface AssessmentAnalysis {
  session_id: string;
  summary: AssessmentSummary;
  performance_by_topic: TopicPerformance[];
  weak_topics: string[];
  strong_topics: string[];
  recommendations: string[];
}

export interface DashboardActivity {
  id: string;
  type: "assessment" | "tutoring" | string;
  capability: string;
  title: string;
  timestamp: number;
  summary: string;
  session_ref: string;
  message_count: number;
  status: string;
  active_turn_id?: string | null;
  knowledge_bases: string[];
  assessment_summary?: AssessmentSummary | null;
  review_ref?: string | null;
  replay_ref?: string | null;
}

export interface DashboardActivityDetailMessage {
  id: number;
  session_id: string;
  role: string;
  content: string;
  capability: string;
  created_at: number;
}

export interface DashboardActivityDetail {
  id: string;
  type: "assessment" | "tutoring" | string;
  capability: string;
  title: string;
  timestamp: number;
  knowledge_bases: string[];
  assessment_summary?: AssessmentSummary | null;
  content: {
    messages: DashboardActivityDetailMessage[];
    active_turns: Array<Record<string, unknown>>;
    status: string;
    summary: string;
  };
}

export interface DashboardOverview {
  totals: {
    total_sessions: number;
    assessments: number;
    tutoring_sessions: number;
    running: number;
    completed: number;
    failed: number;
  };
  knowledge_packs: Array<{
    name: string;
    session_count: number;
  }>;
  analytics: {
    engagement: {
      active_days: number;
      streak_days: number;
      knowledge_packs_used: number;
    };
    assessment_trend: {
      assessments_completed: number;
      average_score_percent: number;
      latest_score_percent: number;
      score_delta: number;
    };
    learning_signals: {
      focus_topics: StudentProgressTopic[];
      mastered_topics: StudentProgressTopic[];
    };
  };
  recent_activity: DashboardActivity[];
}

export interface DashboardOverviewFilters {
  type?: string;
  knowledge_base?: string;
  search?: string;
  min_score?: number;
}

export interface StudentProgressTopic {
  topic: string;
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  accuracy_percent: number;
}

export interface StudentProgressAssessment {
  session_id: string;
  title: string;
  timestamp: number;
  score_percent: number;
  correct_count: number;
  total_questions: number;
  knowledge_bases: string[];
  review_ref?: string | null;
}

export interface StudentProgressPathStep {
  topic: string;
  status: "review" | "next" | string;
  source: "focus_topic" | "learning_objective" | string;
  knowledge_base?: string | null;
}

export interface StudentProgressPoint {
  session_id: string;
  score_percent: number;
  timestamp: number;
}

export interface StudentProgressOverview {
  totals: {
    assessments_completed: number;
    tutoring_sessions: number;
    knowledge_packs_used: number;
    average_score_percent: number;
    streak_days: number;
  };
  focus_topics: StudentProgressTopic[];
  mastered_topics: StudentProgressTopic[];
  score_trend: StudentProgressPoint[];
  recent_assessments: StudentProgressAssessment[];
  suggested_learning_path: StudentProgressPathStep[];
}

async function expectJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getDashboardOverview(
  limit = 50,
  filters: DashboardOverviewFilters = {},
): Promise<DashboardOverview> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (filters.type) params.set("type", filters.type);
  if (filters.knowledge_base) params.set("knowledge_base", filters.knowledge_base);
  if (filters.search) params.set("search", filters.search);
  if (typeof filters.min_score === "number") params.set("min_score", String(filters.min_score));

  const response = await fetch(apiUrl(`/api/v1/dashboard/overview?${params.toString()}`), {
    cache: "no-store",
  });
  return expectJson<DashboardOverview>(response);
}

export async function getAssessmentReview(sessionId: string): Promise<AssessmentReview> {
  const response = await fetch(apiUrl(`/api/v1/sessions/${sessionId}/assessment-review`), {
    cache: "no-store",
  });
  return expectJson<AssessmentReview>(response);
}

export async function getAssessmentAnalysis(sessionId: string): Promise<AssessmentAnalysis> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/assessment-analysis/${sessionId}`), {
    cache: "no-store",
  });
  return expectJson<AssessmentAnalysis>(response);
}

export async function getStudentProgress(limit = 50): Promise<StudentProgressOverview> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/student-progress?limit=${limit}`), {
    cache: "no-store",
  });
  return expectJson<StudentProgressOverview>(response);
}

export async function downloadAssessmentExportPdf(sessionId: string): Promise<Blob> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/assessment-export/${sessionId}`), {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.blob();
}

export async function getDashboardActivityDetail(entryId: string): Promise<DashboardActivityDetail> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/${entryId}`), {
    cache: "no-store",
  });
  return expectJson<DashboardActivityDetail>(response);
}

export interface TeacherInsightStudent {
  student_id: string;
  observed: {
    topic: string;
    miss_count: number;
    avg_latency_seconds: number;
  } | null;
  student_state?: {
    support_level: string;
    confidence_trend: string;
  } | null;
  inferred: Array<{
    diagnosis_type: string;
    confidence_tag: string;
    topic: string;
    evidence: string[];
  }>;
  diagnosis_feedback?: DiagnosisFeedbackRecord | null;
  recommended_actions: Array<{
    action_id: string;
    action_type: string;
    target_student_ids: string[];
    topic: string;
    rationale: string;
  }>;
  recommendation_ack?: RecommendationAckRecord | null;
  teacher_actions?: TeacherActionRecord[];
  intervention_assignments?: InterventionAssignmentRecord[];
  intervention_history?: InterventionHistoryItem[];
}

export type InterventionHistoryItemType =
  | "recommendation_ack"
  | "teacher_action"
  | "intervention_assignment"
  | "diagnosis_feedback";

export interface InterventionHistoryItem {
  id: string;
  item_type: InterventionHistoryItemType;
  timestamp: number;
  title: string;
  detail: string;
  status: string;
  topic: string;
  source_id: string;
}

export type DiagnosisFeedbackLabel = "helpful" | "wrong" | "incomplete";

export interface DiagnosisFeedbackRecord {
  id: string;
  student_id: string;
  source_topic: string;
  source_diagnosis_type: string;
  feedback_label: DiagnosisFeedbackLabel;
  teacher_note: string;
  created_at: number;
  updated_at: number;
}

export type RecommendationAckStatus = "accepted" | "deferred" | "dismissed" | "completed";

export interface RecommendationAckRecord {
  id: string;
  source_recommendation_id: string;
  target_type: "student" | "small_group";
  target_id: string;
  status: RecommendationAckStatus;
  teacher_note: string;
  created_at: number;
  updated_at: number;
}

export type TeacherActionType =
  | "reteach_concept"
  | "scaffolded_practice"
  | "review_prerequisite"
  | "small_group_remediation";

export type TeacherActionStatus = "draft" | "planned" | "done" | "dismissed";

export type TeacherActionPriority = "low" | "medium" | "high";

export interface TeacherActionRecord {
  id: string;
  target_type: "student" | "small_group";
  target_id: string;
  source_recommendation_id: string;
  action_type: TeacherActionType;
  topic: string;
  teacher_instruction: string;
  priority: TeacherActionPriority;
  status: TeacherActionStatus;
  created_at: number;
  updated_at: number;
}

export type InterventionAssignmentType =
  | "practice_set"
  | "reteach_session"
  | "prerequisite_review"
  | "small_group_activity";

export type InterventionAssignmentStatus = "draft" | "planned" | "done" | "dismissed";

export interface InterventionAssignmentRecord {
  id: string;
  teacher_action_id: string;
  target_type: "student" | "small_group";
  target_id: string;
  assignment_type: InterventionAssignmentType;
  topic: string;
  title: string;
  teacher_note: string;
  practice_note: string;
  status: InterventionAssignmentStatus;
  created_at: number;
  updated_at: number;
}

export interface DashboardInsights {
  students: TeacherInsightStudent[];
  small_groups: Array<{
    topic: string;
    diagnosis_type: string;
    student_ids: string[];
    recommended_action: string;
    target_id?: string;
    recommendation_ack?: RecommendationAckRecord | null;
    teacher_action?: TeacherActionRecord | null;
    intervention_assignment?: InterventionAssignmentRecord | null;
  }>;
}

export interface DashboardInsightsFilters {
  knowledge_base?: string;
  start_ts?: number;
  end_ts?: number;
  cohort?: string;
}

export interface CreateTeacherActionRequest {
  target_type: "student" | "small_group";
  target_id: string;
  source_recommendation_id: string;
  action_type: TeacherActionType;
  topic: string;
  teacher_instruction: string;
  priority: TeacherActionPriority;
}

export interface CreateRecommendationAckRequest {
  source_recommendation_id: string;
  target_type: "student" | "small_group";
  target_id: string;
  status: RecommendationAckStatus;
  teacher_note?: string;
}

export interface CreateDiagnosisFeedbackRequest {
  student_id: string;
  source_topic: string;
  source_diagnosis_type: string;
  feedback_label: DiagnosisFeedbackLabel;
  teacher_note?: string;
}

export interface CreateInterventionAssignmentRequest {
  teacher_action_id: string;
  assignment_type: InterventionAssignmentType;
  title: string;
  teacher_note: string;
  practice_note: string;
}

/**
 * Teacher-facing insights: actionable signals and recommendations.
 */
export async function getDashboardInsights(
  limit = 100,
  filters: DashboardInsightsFilters = {},
): Promise<DashboardInsights> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (filters.knowledge_base) params.set("knowledge_base", filters.knowledge_base);
  if (typeof filters.start_ts === "number") params.set("start_ts", String(filters.start_ts));
  if (typeof filters.end_ts === "number") params.set("end_ts", String(filters.end_ts));
  if (filters.cohort) params.set("cohort", filters.cohort);

  const response = await fetch(apiUrl(`/api/v1/dashboard/insights?${params.toString()}`), {
    cache: "no-store",
  });
  return expectJson<DashboardInsights>(response);
}

export async function createTeacherAction(
  payload: CreateTeacherActionRequest,
): Promise<TeacherActionRecord> {
  const response = await fetch(apiUrl("/api/v1/dashboard/teacher-actions"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<TeacherActionRecord>(response);
}

export async function createRecommendationAck(
  payload: CreateRecommendationAckRequest,
): Promise<RecommendationAckRecord> {
  const response = await fetch(apiUrl("/api/v1/dashboard/recommendation-acks"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<RecommendationAckRecord>(response);
}

export async function createDiagnosisFeedback(
  payload: CreateDiagnosisFeedbackRequest,
): Promise<DiagnosisFeedbackRecord> {
  const response = await fetch(apiUrl("/api/v1/dashboard/diagnosis-feedback"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<DiagnosisFeedbackRecord>(response);
}

export async function updateDiagnosisFeedback(
  feedbackId: string,
  payload: { feedback_label: DiagnosisFeedbackLabel; teacher_note?: string },
): Promise<DiagnosisFeedbackRecord> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/diagnosis-feedback/${feedbackId}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<DiagnosisFeedbackRecord>(response);
}

export async function updateRecommendationAck(
  ackId: string,
  payload: { status: RecommendationAckStatus; teacher_note?: string },
): Promise<RecommendationAckRecord> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/recommendation-acks/${ackId}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<RecommendationAckRecord>(response);
}

export async function updateTeacherActionStatus(
  actionId: string,
  status: TeacherActionStatus,
): Promise<TeacherActionRecord> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/teacher-actions/${actionId}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  return expectJson<TeacherActionRecord>(response);
}

export async function createInterventionAssignment(
  payload: CreateInterventionAssignmentRequest,
): Promise<InterventionAssignmentRecord> {
  const response = await fetch(apiUrl("/api/v1/dashboard/intervention-assignments"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<InterventionAssignmentRecord>(response);
}

export async function updateInterventionAssignmentStatus(
  assignmentId: string,
  status: InterventionAssignmentStatus,
): Promise<InterventionAssignmentRecord> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/intervention-assignments/${assignmentId}`), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  return expectJson<InterventionAssignmentRecord>(response);
}
