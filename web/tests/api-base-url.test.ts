import { afterEach, describe, expect, it, vi } from "vitest";

const ORIGINAL_EXTERNAL = process.env.NEXT_PUBLIC_API_BASE_EXTERNAL;
const ORIGINAL_INTERNAL = process.env.NEXT_PUBLIC_API_BASE;

async function importApiModule() {
  return import("../lib/api");
}

afterEach(() => {
  vi.resetModules();
  if (ORIGINAL_EXTERNAL === undefined) {
    delete process.env.NEXT_PUBLIC_API_BASE_EXTERNAL;
  } else {
    process.env.NEXT_PUBLIC_API_BASE_EXTERNAL = ORIGINAL_EXTERNAL;
  }

  if (ORIGINAL_INTERNAL === undefined) {
    delete process.env.NEXT_PUBLIC_API_BASE;
  } else {
    process.env.NEXT_PUBLIC_API_BASE = ORIGINAL_INTERNAL;
  }
});

describe("api base url", () => {
  it("prefers NEXT_PUBLIC_API_BASE_EXTERNAL over NEXT_PUBLIC_API_BASE", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_EXTERNAL", "https://contest.example/api");
    vi.stubEnv("NEXT_PUBLIC_API_BASE", "http://localhost:8001");

    const { API_BASE_URL, apiUrl } = await importApiModule();

    expect(API_BASE_URL).toBe("https://contest.example/api");
    expect(apiUrl("/api/v1/dashboard/overview")).toBe(
      "https://contest.example/api/api/v1/dashboard/overview",
    );
  });

  it("defaults protected api fetches to include auth cookies", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_EXTERNAL", "https://contest.example/api");
    const fetchSpy = vi.fn().mockResolvedValue(new Response(null, { status: 204 }));
    vi.stubGlobal("fetch", fetchSpy);

    const { apiFetch } = await importApiModule();

    await apiFetch("/api/v1/knowledge/list", { cache: "no-store" });

    expect(fetchSpy).toHaveBeenCalledWith(
      "https://contest.example/api/api/v1/knowledge/list",
      expect.objectContaining({
        cache: "no-store",
        credentials: "include",
      }),
    );
  });

  it("lets callers override credentials explicitly when needed", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_EXTERNAL", "https://contest.example/api");
    const fetchSpy = vi.fn().mockResolvedValue(new Response(null, { status: 204 }));
    vi.stubGlobal("fetch", fetchSpy);

    const { apiFetch } = await importApiModule();

    await apiFetch("/api/v1/auth/verify-email", {
      method: "POST",
      credentials: "omit",
    });

    expect(fetchSpy).toHaveBeenCalledWith(
      "https://contest.example/api/api/v1/auth/verify-email",
      expect.objectContaining({
        method: "POST",
        credentials: "omit",
      }),
    );
  });
});
