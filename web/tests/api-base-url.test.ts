import assert from "node:assert/strict";
import test from "node:test";

const ORIGINAL_EXTERNAL = process.env.NEXT_PUBLIC_API_BASE_EXTERNAL;
const ORIGINAL_INTERNAL = process.env.NEXT_PUBLIC_API_BASE;

async function importApiModule() {
  const moduleUrl = new URL(`../lib/api.ts?case=${Math.random()}`, import.meta.url).href;
  return import(moduleUrl);
}

test("apiUrl prefers NEXT_PUBLIC_API_BASE_EXTERNAL over NEXT_PUBLIC_API_BASE", async (t) => {
  t.after(() => {
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

  process.env.NEXT_PUBLIC_API_BASE_EXTERNAL = "https://contest.example/api";
  process.env.NEXT_PUBLIC_API_BASE = "http://localhost:8001";

  const { API_BASE_URL, apiUrl } = await importApiModule();

  assert.equal(API_BASE_URL, "https://contest.example/api");
  assert.equal(apiUrl("/api/v1/dashboard/overview"), "https://contest.example/api/api/v1/dashboard/overview");
});
