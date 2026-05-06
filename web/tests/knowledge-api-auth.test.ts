import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("../lib/offline-pack-cache", () => ({
  listOfflineImportedPacks: vi.fn(() => [
    {
      name: "offline-pack",
      imported_at: "2026-05-06T00:00:00Z",
      metadata: { subject: "Toán" },
    },
  ]),
}));

async function importKnowledgeApi() {
  return import("../lib/knowledge-api");
}

afterEach(() => {
  vi.resetModules();
  vi.unstubAllGlobals();
  window.localStorage.clear();
});

describe("knowledge api auth behavior", () => {
  it("does not swallow a 401 list response into an empty or offline list", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Authentication required" }), {
          status: 401,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    const { listKnowledgeBases } = await importKnowledgeApi();

    await expect(listKnowledgeBases({ force: true })).rejects.toThrow(
      "Authentication required",
    );
  });

  it("still falls back to offline imported packs for genuine network failures", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch")),
    );

    const { listKnowledgeBases } = await importKnowledgeApi();

    await expect(listKnowledgeBases({ force: true })).resolves.toEqual([
      expect.objectContaining({
        name: "offline-pack",
        status: "offline-cached",
      }),
    ]);
  });
});
