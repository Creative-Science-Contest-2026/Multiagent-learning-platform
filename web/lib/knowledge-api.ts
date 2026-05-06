import { apiFetch } from "@/lib/api";
import { invalidateClientCache, withClientCache } from "@/lib/client-cache";
import { listOfflineImportedPacks } from "@/lib/offline-pack-cache";

const KNOWLEDGE_CACHE_PREFIX = "knowledge:";

export interface TeacherPackMetadata {
  subject?: string | null;
  grade?: string | null;
  curriculum?: string | null;
  learning_objectives?: string[] | null;
  owner?: string | null;
  sharing_status?: "private" | "team" | "public" | null;
  team_members?: string[] | null;
  pending_invites?: string[] | null;
  tags?: string[] | null;
  difficulty?: "beginner" | "intermediate" | "advanced" | null;
  language?: string | null;
  estimated_hours?: number | null;
  prerequisites?: string[] | null;
  content_types?: string[] | null;
}

export interface KnowledgeProgressSummary {
  task_id?: string;
  stage?: string;
  message?: string;
  current?: number;
  total?: number;
  percent?: number;
  progress_percent?: number;
  file_name?: string;
  file_statuses?: Array<{
    name: string;
    status: string;
    updated_at?: string;
    error?: string;
  }>;
  error?: string;
  timestamp?: string;
}

export interface KnowledgeBaseStatisticsSummary {
  raw_documents?: number;
  rag_provider?: string;
  needs_reindex?: boolean;
  status?: string;
  progress?: KnowledgeProgressSummary;
  [key: string]: unknown;
}

export interface KnowledgeBaseSummary {
  name: string;
  is_default?: boolean;
  status?: string;
  progress?: KnowledgeProgressSummary;
  statistics?: KnowledgeBaseStatisticsSummary;
  metadata?: TeacherPackMetadata | null;
}

export interface RagProviderSummary {
  id: string;
  name: string;
  description: string;
}

async function expectJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    const detail = typeof error?.detail === "string" ? error.detail : "";
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function listKnowledgeBases(options?: { force?: boolean }) {
  return withClientCache<KnowledgeBaseSummary[]>(
    `${KNOWLEDGE_CACHE_PREFIX}list`,
    async () => {
      try {
        const response = await apiFetch("/api/v1/knowledge/list", {
          cache: "no-store",
        });
        const data = await expectJson<KnowledgeBaseSummary[] | { knowledge_bases?: KnowledgeBaseSummary[] }>(response);
        return Array.isArray(data)
          ? data
          : Array.isArray(data?.knowledge_bases)
            ? data.knowledge_bases
            : [];
      } catch (error) {
        if (!(error instanceof TypeError)) {
          throw error;
        }
        return listOfflineImportedPacks().map((pack) => ({
          name: pack.name,
          is_default: false,
          status: "offline-cached",
          metadata: pack.metadata ?? null,
        }));
      }
    },
    {
      force: options?.force,
    },
  );
}

export async function listRagProviders(options?: { force?: boolean }) {
  return withClientCache<RagProviderSummary[]>(
    `${KNOWLEDGE_CACHE_PREFIX}providers`,
    async () => {
      const response = await apiFetch("/api/v1/knowledge/rag-providers", {
        cache: "no-store",
      });
      const data = await expectJson<{ providers?: RagProviderSummary[] }>(response);
      return Array.isArray(data?.providers) ? data.providers : [];
    },
    {
      force: options?.force,
    },
  );
}

export async function updateKnowledgeBaseConfig(
  kbName: string,
  config: TeacherPackMetadata | Record<string, unknown>,
) {
  const response = await apiFetch(`/api/v1/knowledge/${encodeURIComponent(kbName)}/config`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(config),
  });

  invalidateKnowledgeCaches();
  return expectJson(response);
}

export function invalidateKnowledgeCaches() {
  invalidateClientCache(KNOWLEDGE_CACHE_PREFIX);
}
