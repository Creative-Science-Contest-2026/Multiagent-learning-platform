import { apiUrl } from "@/lib/api";

export interface MarketplacePackMetadata {
  subject?: string | null;
  grade?: string | null;
  curriculum?: string | null;
  learning_objectives?: string[] | null;
  owner?: string | null;
  sharing_status?: "private" | "team" | "public" | null;
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

export async function listMarketplacePacks(
  sharingStatus?: string,
  subject?: string,
  owner?: string,
  sortBy?: MarketplaceSortBy,
  limit = 50,
  offset = 0,
): Promise<MarketplaceListResponse> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  if (sharingStatus) params.append("sharing_status", sharingStatus);
  if (subject) params.append("subject", subject);
  if (owner) params.append("owner", owner);
  if (sortBy) params.append("sort_by", sortBy);

  const response = await fetch(apiUrl(`/api/v1/marketplace/list?${params}`), {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch marketplace packs: ${response.status}`);
  }

  return response.json();
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

  return response.json();
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

  return response.json();
}
