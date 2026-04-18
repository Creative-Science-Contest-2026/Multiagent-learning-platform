import { apiUrl } from "@/lib/api";

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
