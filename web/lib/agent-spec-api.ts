import { apiUrl } from "@/lib/api";

export interface AgentSpecSummary {
  agent_id: string;
  display_name: string;
  description: string;
  version: number;
  updated_at: string;
}

export interface AgentSpecStructuredIdentity {
  agent_name: string;
  subject: string;
  grade_band: string;
  tone: string;
  primary_language: string;
  persona_summary: string;
}

export interface AgentSpecStructuredSoul {
  teaching_philosophy: string;
  when_student_wrong: string;
  when_student_stuck: string;
  encouragement_style: string;
}

export interface AgentSpecStructuredRules {
  do_not_solve_directly: string;
  max_session_minutes: string;
  hint_policy: string;
  escalation_rule: string;
  guardrails: string;
}

export interface AgentSpecDetail {
  agent_id: string;
  display_name: string;
  description: string;
  version: number;
  created_at?: string;
  updated_at?: string;
  files: Record<string, string>;
  structured: {
    identity: AgentSpecStructuredIdentity;
    soul: AgentSpecStructuredSoul;
    rules: AgentSpecStructuredRules;
  };
  summary: {
    subject: string;
    language: string;
    teaching_philosophy: string;
    guardrails: string;
  };
}

export interface AgentSpecUpsertPayload {
  agent_id: string;
  display_name: string;
  description: string;
  structured: AgentSpecDetail["structured"];
  files: Record<string, string>;
}

export interface RuntimePolicyAuditPayload {
  agent_spec_id: string;
  agent_spec_version: number | null;
  capability: string;
  runtime_policy: {
    capability: string;
    agent_spec_id: string;
    agent_spec_version: number | null;
    slices: Record<string, string>;
    sources: Record<string, string>;
    knowledge_policy: string;
    source_priority: string[];
    teacher_kb_context: string;
    debug: {
      applied_slices: string[];
      missing_slices: string[];
      slice_sources: Record<string, string>;
      agent_spec_id: string;
      agent_spec_version: number | null;
      has_teacher_kb_context: boolean;
    };
  };
}

async function expectJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function listAgentSpecs(): Promise<AgentSpecSummary[]> {
  const response = await fetch(apiUrl("/api/v1/agent-specs"), { cache: "no-store" });
  const payload = await expectJson<{ items: AgentSpecSummary[] }>(response);
  return payload.items;
}

export async function getAgentSpec(agentId: string): Promise<AgentSpecDetail> {
  const response = await fetch(apiUrl(`/api/v1/agent-specs/${agentId}`), { cache: "no-store" });
  return expectJson<AgentSpecDetail>(response);
}

export async function createAgentSpec(payload: AgentSpecUpsertPayload): Promise<AgentSpecDetail> {
  const response = await fetch(apiUrl("/api/v1/agent-specs"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<AgentSpecDetail>(response);
}

export async function updateAgentSpec(agentId: string, payload: AgentSpecUpsertPayload): Promise<AgentSpecDetail> {
  const response = await fetch(apiUrl(`/api/v1/agent-specs/${agentId}`), {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return expectJson<AgentSpecDetail>(response);
}

export async function exportAgentSpec(agentId: string): Promise<Blob> {
  const response = await fetch(apiUrl(`/api/v1/agent-specs/${agentId}/export`), { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Export failed: ${response.status}`);
  }
  return response.blob();
}

export async function getAgentSpecRuntimePolicyAudit(
  agentId: string,
  capability = "chat",
): Promise<RuntimePolicyAuditPayload> {
  const response = await fetch(
    apiUrl(`/api/v1/agent-specs/${agentId}/runtime-policy-audit?capability=${encodeURIComponent(capability)}`),
    { cache: "no-store" },
  );
  return expectJson<RuntimePolicyAuditPayload>(response);
}
