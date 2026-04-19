import { apiUrl } from "@/lib/api";

export interface AssessmentSummary {
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  score_percent: number;
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

async function expectJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getDashboardOverview(limit = 50): Promise<DashboardOverview> {
  const response = await fetch(apiUrl(`/api/v1/dashboard/overview?limit=${limit}`), {
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
