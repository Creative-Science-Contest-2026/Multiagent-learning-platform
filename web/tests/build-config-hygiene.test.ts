import { readFileSync } from "node:fs";
import path from "node:path";

import { describe, expect, it } from "vitest";

const tsconfig = JSON.parse(
  readFileSync(path.resolve(__dirname, "../tsconfig.json"), "utf-8"),
) as {
  exclude?: string[];
};

const nextConfigSource = readFileSync(
  path.resolve(__dirname, "../next.config.js"),
  "utf-8",
);

describe("frontend build hygiene config", () => {
  it("keeps test-only inputs out of the app TypeScript compile path", () => {
    expect(tsconfig.exclude).toEqual(
      expect.arrayContaining([
        "tests",
        "tests/**",
        "vitest.config.ts",
        "playwright.config.ts",
      ]),
    );
  });

  it("pins turbopack root to the web workspace", () => {
    expect(nextConfigSource).toContain("root: __dirname");
  });
});
