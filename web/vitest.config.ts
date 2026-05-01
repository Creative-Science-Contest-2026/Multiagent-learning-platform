import path from "node:path";

import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup-vitest.ts"],
    include: [
      "tests/api-base-url.test.ts",
      "tests/class-tutor-pack-presenters.test.ts",
      "tests/knowledge-page-wizard-shell.test.ts",
      "tests/markdown-display.test.ts",
      "tests/playground-trace.test.ts",
      "tests/sidebar-nav-groups.test.ts",
      "tests/teacher-cockpit-content.test.ts",
      "tests/teacher-dashboard-copy.test.ts",
      "tests/teacher-dashboard-decision-flow.test.ts",
    ],
    coverage: {
      provider: "v8",
      reporter: ["text", "json-summary"],
      reportsDirectory: "./coverage",
      include: [
        "components/agents/class-tutor-pack-presenters.ts",
        "components/contest/teacher-cockpit-content.ts",
        "components/dashboard/dashboard-presenters.ts",
        "components/sidebar/nav-groups.ts",
        "lib/api.ts",
        "lib/markdown-display.ts",
        "lib/playground-trace.ts",
      ],
      thresholds: {
        lines: 80,
        statements: 80,
        functions: 80,
        branches: 70,
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "."),
    },
  },
});
