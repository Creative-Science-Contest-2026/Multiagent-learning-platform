import { apiUrl } from "@/lib/api";

export interface AssessmentSummary {
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  score_percent: number;
  estimated_time_spent?: number;
}

export interface AssessmentReviewResult {
  question_id: string;
  question: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
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
