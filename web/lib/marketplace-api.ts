import { apiUrl } from "@/lib/api";
import { cacheImportedPack } from "@/lib/offline-pack-cache";

export interface MarketplacePackMetadata {
  subject?: string | null;
  grade?: string | null;
  curriculum?: string | null;
  learning_objectives?: string[] | null;
  owner?: string | null;
  sharing_status?: "private" | "team" | "public" | null;
  tags?: string[] | null;
  difficulty?: "beginner" | "intermediate" | "advanced" | null;
  language?: string | null;
  estimated_hours?: number | null;
  prerequisites?: string[] | null;
  content_types?: string[] | null;
}

export interface MarketplaceRatingSummary {
  average_rating: number;
  review_count: number;
}

export interface MarketplaceReview {
  reviewer: string;
  rating: number;
  comment?: string | null;
  created_at: string;
}

export interface MarketplacePack {
  name: string;
  subject?: string | null;
  grade?: string | null;
  curriculum?: string | null;
  learning_objectives?: string[] | null;
  owner?: string | null;
  sharing_status?: "public" | "team" | null;
  session_count?: number;
  status?: string;
  rating_summary?: MarketplaceRatingSummary;
  tags?: string[] | null;
  difficulty?: "beginner" | "intermediate" | "advanced" | null;
  language?: string | null;
  estimated_hours?: number | null;
  prerequisites?: string[] | null;
  content_types?: string[] | null;
}

export interface MarketplacePackPreview extends MarketplacePack {
  description?: string | null;
  document_count: number;
  sample_documents: string[];
  recent_reviews: MarketplaceReview[];
}

export interface MarketplaceListResponse {
  total: number;
  offset: number;
  limit: number;
  packs: MarketplacePack[];
}

export type MarketplaceSortBy =
  | "popularity"
  | "recent"
  | "rating"
  | "most_objectives";

export interface MarketplaceListFetchOptions {
  forceRefresh?: boolean;
}

interface MarketplaceListCacheEntry {
  data?: MarketplaceListResponse;
  updatedAt: number;
  promise?: Promise<MarketplaceListResponse>;
}

const MARKETPLACE_LIST_CACHE_TTL_MS = 5 * 60 * 1000;
const marketplaceListCache = new Map<string, MarketplaceListCacheEntry>();

function buildMarketplaceListCacheKey(
  search?: string,
  sharingStatus?: string,
  subject?: string,
  owner?: string,
  sortBy?: MarketplaceSortBy,
  limit = 50,
  offset = 0,
): string {
  return JSON.stringify({
    search: search || "",
    sharingStatus: sharingStatus || "",
    subject: subject || "",
    owner: owner || "",
    sortBy: sortBy || "",
    limit,
    offset,
  });
}

function isMarketplaceListCacheFresh(entry?: MarketplaceListCacheEntry): boolean {
  return Boolean(entry?.data && Date.now() - entry.updatedAt < MARKETPLACE_LIST_CACHE_TTL_MS);
}

export function getCachedMarketplacePacks(
  search?: string,
  sharingStatus?: string,
  subject?: string,
  owner?: string,
  sortBy?: MarketplaceSortBy,
  limit = 50,
  offset = 0,
): MarketplaceListResponse | null {
  const cacheKey = buildMarketplaceListCacheKey(
    search,
    sharingStatus,
    subject,
    owner,
    sortBy,
    limit,
    offset,
  );
  return marketplaceListCache.get(cacheKey)?.data ?? null;
}

export function isMarketplacePacksCacheStale(
  search?: string,
  sharingStatus?: string,
  subject?: string,
  owner?: string,
  sortBy?: MarketplaceSortBy,
  limit = 50,
  offset = 0,
): boolean {
  const cacheKey = buildMarketplaceListCacheKey(
    search,
    sharingStatus,
    subject,
    owner,
    sortBy,
    limit,
    offset,
  );
  return !isMarketplaceListCacheFresh(marketplaceListCache.get(cacheKey));
}

export function invalidateMarketplaceListCache(): void {
  marketplaceListCache.clear();
}

export async function listMarketplacePacks(
  search?: string,
  sharingStatus?: string,
  subject?: string,
  owner?: string,
  sortBy?: MarketplaceSortBy,
  limit = 50,
  offset = 0,
  options: MarketplaceListFetchOptions = {},
): Promise<MarketplaceListResponse> {
  const cacheKey = buildMarketplaceListCacheKey(
    search,
    sharingStatus,
    subject,
    owner,
    sortBy,
    limit,
    offset,
  );
  const existingEntry = marketplaceListCache.get(cacheKey);

  if (!options.forceRefresh) {
    if (isMarketplaceListCacheFresh(existingEntry)) {
      return existingEntry!.data!;
    }
    if (existingEntry?.promise) {
      return existingEntry.promise;
    }
  }

  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  if (sharingStatus) params.append("sharing_status", sharingStatus);
  if (search) params.append("search", search);
  if (subject) params.append("subject", subject);
  if (owner) params.append("owner", owner);
  if (sortBy) params.append("sort_by", sortBy);

  const request = fetch(apiUrl(`/api/v1/marketplace/list?${params}`), {
    cache: "no-store",
  }).then(async (response) => {
    if (!response.ok) {
      throw new Error(`Failed to fetch marketplace packs: ${response.status}`);
    }

    const data = (await response.json()) as MarketplaceListResponse;
    marketplaceListCache.set(cacheKey, {
      data,
      updatedAt: Date.now(),
    });
    return data;
  }).catch((error) => {
    if (existingEntry?.data) {
      marketplaceListCache.set(cacheKey, existingEntry);
    } else {
      marketplaceListCache.delete(cacheKey);
    }
    throw error;
  });

  marketplaceListCache.set(cacheKey, {
    data: existingEntry?.data,
    updatedAt: existingEntry?.updatedAt ?? 0,
    promise: request,
  });

  return request;
}

export async function getMarketplacePack(packName: string): Promise<MarketplacePack> {
  const response = await fetch(
    apiUrl(`/api/v1/marketplace/${encodeURIComponent(packName)}`),
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch marketplace pack: ${response.status}`);
  }

  return response.json();
}

export async function getMarketplacePackPreview(
  packName: string,
): Promise<MarketplacePackPreview> {
  const response = await fetch(
    apiUrl(`/api/v1/marketplace/${encodeURIComponent(packName)}/preview`),
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch marketplace preview: ${response.status}`);
  }

  return response.json();
}


export interface ImportPackResult {
  success: boolean;
  message: string;
  pack: {
    name: string;
    subject?: string;
    grade?: string;
    owner?: string;
    import_date: string;
    session_count?: number;
  };
}

export interface BatchImportPackResult {
  source_pack: string;
  success: boolean;
  message: string;
  pack: ImportPackResult["pack"] | null;
}

export interface BatchImportPacksResult {
  success: boolean;
  requested: number;
  imported: number;
  results: BatchImportPackResult[];
}

export interface SubmitMarketplaceReviewRequest {
  reviewer: string;
  rating: number;
  comment?: string;
}

export interface SubmitMarketplaceReviewResult {
  success: boolean;
  review: MarketplaceReview;
  rating_summary: MarketplaceRatingSummary;
}

export async function importMarketplacePack(
  packName: string,
): Promise<ImportPackResult> {
  const response = await fetch(
    apiUrl(`/api/v1/marketplace/import/${encodeURIComponent(packName)}`),
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    },
  );

  if (!response.ok) {
    const errorBody = await response.text();
    try {
      const error = JSON.parse(errorBody);
      throw new Error(error.detail || `Failed to import pack: ${response.status}`);
    } catch {
      throw new Error(`Failed to import pack: ${response.status} ${response.statusText}`);
    }
  }

  const result = await response.json();
  cacheImportedPack({
    name: result.pack.name,
    imported_at: result.pack.import_date,
    metadata: {
      subject: result.pack.subject ?? null,
      grade: result.pack.grade ?? null,
      owner: result.pack.owner ?? null,
      sharing_status: "private",
    },
  });
  invalidateMarketplaceListCache();
  return result;
}

export async function importMarketplacePacks(
  packNames: string[],
): Promise<BatchImportPacksResult> {
  const response = await fetch(
    apiUrl("/api/v1/marketplace/import-batch"),
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pack_names: packNames }),
    },
  );

  if (!response.ok) {
    const errorBody = await response.text();
    try {
      const error = JSON.parse(errorBody);
      throw new Error(error.detail || `Failed to import packs: ${response.status}`);
    } catch {
      throw new Error(`Failed to import packs: ${response.status} ${response.statusText}`);
    }
  }

  const result = (await response.json()) as BatchImportPacksResult;
  result.results
    .filter((row) => row.success && row.pack)
    .forEach((row) => {
      cacheImportedPack({
        name: row.pack!.name,
        imported_at: row.pack!.import_date,
        metadata: {
          subject: row.pack!.subject ?? null,
          grade: row.pack!.grade ?? null,
          owner: row.pack!.owner ?? null,
          sharing_status: "private",
        },
      });
    });
  invalidateMarketplaceListCache();
  return result;
}

export async function submitMarketplaceReview(
  packName: string,
  payload: SubmitMarketplaceReviewRequest,
): Promise<SubmitMarketplaceReviewResult> {
  const response = await fetch(
    apiUrl(`/api/v1/marketplace/${encodeURIComponent(packName)}/reviews`),
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    const errorBody = await response.text();
    try {
      const error = JSON.parse(errorBody);
      throw new Error(error.detail || `Failed to submit review: ${response.status}`);
    } catch {
      throw new Error(`Failed to submit review: ${response.status} ${response.statusText}`);
    }
  }

  const result = await response.json();
  invalidateMarketplaceListCache();
  return result;
}
