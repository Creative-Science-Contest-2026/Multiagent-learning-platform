import type { TeacherPackMetadata } from "@/lib/knowledge-api";

const OFFLINE_IMPORTED_PACKS_KEY = "deeptutor:offline-imported-packs";

export interface OfflineImportedPack {
  name: string;
  imported_at: string;
  metadata?: TeacherPackMetadata | null;
}

function canUseStorage(): boolean {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function readOfflineImportedPacks(): OfflineImportedPack[] {
  if (!canUseStorage()) return [];
  try {
    const raw = window.localStorage.getItem(OFFLINE_IMPORTED_PACKS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    return Array.isArray(parsed)
      ? parsed.filter((item): item is OfflineImportedPack => Boolean(item && typeof item === "object"))
      : [];
  } catch {
    return [];
  }
}

function writeOfflineImportedPacks(packs: OfflineImportedPack[]): void {
  if (!canUseStorage()) return;
  window.localStorage.setItem(OFFLINE_IMPORTED_PACKS_KEY, JSON.stringify(packs));
}

export function cacheImportedPack(pack: OfflineImportedPack): void {
  const existing = readOfflineImportedPacks().filter((item) => item.name !== pack.name);
  existing.unshift(pack);
  writeOfflineImportedPacks(existing.slice(0, 100));
}

export function listOfflineImportedPacks(): OfflineImportedPack[] {
  return readOfflineImportedPacks();
}
