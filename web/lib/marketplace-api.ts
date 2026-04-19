import { apiUrl } from "@/lib/api";

export interface MarketplacePackMetadata {
  subject?: string | null;
  grade?: string | null;
  curriculum?: string | null;
  learning_objectives?: string[] | null;
  owner?: string | null;
  sharing_status?: "private" | "team" | "public" | null;
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
}

export interface MarketplaceListResponse {
  total: number;
  offset: number;
  limit: number;
  packs: MarketplacePack[];
}

export async function listMarketplacePacks(
  sharingStatus?: string,
  subject?: string,
  owner?: string,
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
