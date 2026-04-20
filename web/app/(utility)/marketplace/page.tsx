"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { BookOpen, Download, Filter, Loader2, Search } from "lucide-react";
import { useTranslation } from "react-i18next";
import {
  listMarketplacePacks,
  importMarketplacePack,
  type MarketplaceListResponse,
  type MarketplacePack,
} from "@/lib/marketplace-api";

export default function MarketplacePage() {
  const { t } = useTranslation();
  const [packs, setPacks] = useState<MarketplacePack[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [searchTerm, setSearchTerm] = useState("");
  const [filterSubject, setFilterSubject] = useState("");
  const [filterOwner, setFilterOwner] = useState("");
  const [sharingStatus, setSharingStatus] = useState<"public" | "team" | undefined>(undefined);

  // Pagination
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const limit = 20;

  // Import state
  const [importing, setImporting] = useState<string | null>(null);
  const [importSuccess, setImportSuccess] = useState<string | null>(null);

  const loadPacks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response: MarketplaceListResponse = await listMarketplacePacks(
        sharingStatus,
        filterSubject || undefined,
        filterOwner || undefined,
        limit,
        offset,
      );
      setPacks(response.packs);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load marketplace");
      setPacks([]);
    } finally {
      setLoading(false);
    }
  }, [filterOwner, filterSubject, limit, offset, sharingStatus]);

  useEffect(() => {
    loadPacks();
  }, [loadPacks]);

  const handleImportPack = async (packName: string) => {
    setImporting(packName);
    try {
      await importMarketplacePack(packName);
      setImportSuccess(packName);
      setTimeout(() => setImportSuccess(null), 3000);
      await loadPacks();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to import pack");
    } finally {
      setImporting(null);
    }
  };

  const filteredPacks = packs.filter((pack) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return (
      pack.name.toLowerCase().includes(term) ||
      pack.subject?.toLowerCase().includes(term) ||
      pack.owner?.toLowerCase().includes(term)
    );
  });

  return (
    <main className="h-full overflow-y-auto bg-[var(--background)]">
      <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-6 px-6 py-8">
        {/* Header */}
        <header>
          <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
            {t("Knowledge Marketplace")}
          </p>
          <h1 className="mt-2 text-[28px] font-semibold tracking-tight text-[var(--foreground)]">
            {t("Discover & Import Knowledge Packs")}
          </h1>
          <p className="mt-2 max-w-[680px] text-[14px] leading-6 text-[var(--muted-foreground)]">
            {t("Browse knowledge packs shared by other teachers and import them to your workspace.")}
          </p>
        </header>

        {/* Filters */}
        <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4">
          <div className="mb-3 flex items-center gap-2 text-[13px] font-medium text-[var(--muted-foreground)]">
            <Filter size={14} />
            {t("Filters")}
          </div>

          <div className="grid gap-3 md:grid-cols-4">
            <div>
              <label className="block text-[12px] font-medium text-[var(--foreground)] mb-1">
                {t("Search")}
              </label>
              <input
                type="text"
                placeholder={t("Pack name, subject...")}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              />
            </div>

            <div>
              <label className="block text-[12px] font-medium text-[var(--foreground)] mb-1">
                {t("Subject")}
              </label>
              <input
                type="text"
                placeholder={t("e.g. Math")}
                value={filterSubject}
                onChange={(e) => setFilterSubject(e.target.value)}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              />
            </div>

            <div>
              <label className="block text-[12px] font-medium text-[var(--foreground)] mb-1">
                {t("Owner")}
              </label>
              <input
                type="text"
                placeholder={t("Teacher name")}
                value={filterOwner}
                onChange={(e) => setFilterOwner(e.target.value)}
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              />
            </div>

            <div>
              <label className="block text-[12px] font-medium text-[var(--foreground)] mb-1">
                {t("Sharing Status")}
              </label>
              <select
                value={sharingStatus || ""}
                onChange={(e) =>
                  setSharingStatus(
                    e.target.value ? (e.target.value as "public" | "team") : undefined,
                  )
                }
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px]"
              >
                <option value="">{t("All")}</option>
                <option value="public">{t("Public")}</option>
                <option value="team">{t("Team")}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {error}
          </div>
        )}

        {/* Packs Grid */}
        <div>
          <div className="mb-3 flex items-center justify-between">
            <span className="text-[13px] text-[var(--muted-foreground)]">
              {t("Showing")} {filteredPacks.length} {t("of")} {total} {t("packs")}
            </span>
            {loading && (
              <span className="flex items-center gap-2 text-[12px] text-[var(--muted-foreground)]">
                <Loader2 size={13} className="animate-spin" />
                {t("Loading")}
              </span>
            )}
          </div>

          {loading ? (
            <div className="flex justify-center py-12">
              <Loader2 size={24} className="animate-spin text-[var(--muted-foreground)]" />
            </div>
          ) : filteredPacks.length === 0 ? (
            <div className="rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-12 text-center">
              <BookOpen size={32} className="mx-auto mb-3 text-[var(--muted-foreground)]" />
              <p className="text-[14px] font-medium text-[var(--foreground)]">
                {t("No knowledge packs found")}
              </p>
              <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">
                {t("Try adjusting your filters or search term")}
              </p>
            </div>
          ) : (
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
              {filteredPacks.map((pack) => (
                <div
                  key={pack.name}
                  className="flex flex-col rounded-lg border border-[var(--border)] bg-[var(--card)] p-4 transition-colors hover:border-[var(--foreground)]/30"
                >
                  {/* Header */}
                  <div className="mb-3 flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-[14px] font-semibold text-[var(--foreground)]">
                        {pack.name}
                      </h3>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {pack.subject && (
                          <span className="inline-block rounded-full bg-[var(--muted)] px-2 py-1 text-[11px] text-[var(--muted-foreground)]">
                            {pack.subject}
                          </span>
                        )}
                        {pack.grade && (
                          <span className="inline-block rounded-full bg-[var(--muted)] px-2 py-1 text-[11px] text-[var(--muted-foreground)]">
                            {pack.grade}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Metadata */}
                  <div className="mb-4 flex-1 space-y-1">
                    {pack.owner && (
                      <p className="text-[12px] text-[var(--muted-foreground)]">
                        <span className="font-medium">{t("By")}:</span> {pack.owner}
                      </p>
                    )}
                    {pack.curriculum && (
                      <p className="text-[12px] text-[var(--muted-foreground)]">
                        <span className="font-medium">{t("Curriculum")}:</span> {pack.curriculum}
                      </p>
                    )}
                    <p className="text-[12px] text-[var(--muted-foreground)]">
                      <span className="font-medium">{t("Sessions")}:</span> {pack.session_count || 0}
                    </p>
                  </div>

                  {/* Learning Objectives */}
                  {pack.learning_objectives && pack.learning_objectives.length > 0 && (
                    <div className="mb-4 rounded-md bg-[var(--background)] p-2">
                      <p className="text-[11px] font-medium text-[var(--muted-foreground)]">
                        {t("Learning Objectives")}:
                      </p>
                      <ul className="mt-1 list-inside list-disc space-y-1">
                        {pack.learning_objectives.slice(0, 2).map((obj, idx) => (
                          <li key={idx} className="text-[11px] text-[var(--foreground)]">
                            {obj}
                          </li>
                        ))}
                        {pack.learning_objectives.length > 2 && (
                          <li className="text-[11px] text-[var(--muted-foreground)]">
                            +{pack.learning_objectives.length - 2} {t("more")}
                          </li>
                        )}
                      </ul>
                    </div>
                  )}

                  {/* Import Button */}
                  <button
                    onClick={() => handleImportPack(pack.name)}
                    disabled={importing === pack.name || importSuccess === pack.name}
                    className="flex items-center justify-center gap-2 rounded-md bg-[var(--primary)] px-3 py-2 text-[12px] font-medium text-[var(--primary-foreground)] transition-opacity hover:opacity-90 disabled:opacity-50"
                  >
                    {importing === pack.name ? (
                      <>
                        <Loader2 size={13} className="animate-spin" />
                        {t("Importing")}
                      </>
                    ) : importSuccess === pack.name ? (
                      <>{t("Imported!")}</>
                    ) : (
                      <>
                        <Download size={13} />
                        {t("Import")}
                      </>
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pagination */}
        {total > limit && (
          <div className="flex items-center justify-center gap-2">
            <button
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
              className="rounded-md border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[12px] disabled:opacity-50"
            >
              {t("Previous")}
            </button>
            <span className="text-[12px] text-[var(--muted-foreground)]">
              {t("Page")} {Math.floor(offset / limit) + 1} {t("of")}{" "}
              {Math.ceil(total / limit)}
            </span>
            <button
              onClick={() => setOffset(offset + limit)}
              disabled={offset + limit >= total}
              className="rounded-md border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[12px] disabled:opacity-50"
            >
              {t("Next")}
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
