import { readFileSync } from "node:fs";
import path from "node:path";

import { describe, expect, it } from "vitest";

const workspaceLayout = readFileSync(path.resolve(__dirname, "../app/(workspace)/layout.tsx"), "utf-8");
const utilityLayout = readFileSync(path.resolve(__dirname, "../app/(utility)/layout.tsx"), "utf-8");

describe("shared shell layouts", () => {
  it("guard the workspace shell with TeacherSurfaceGate", () => {
    expect(workspaceLayout).toContain("TeacherSurfaceGate");
  });

  it("guard the utility shell with TeacherSurfaceGate", () => {
    expect(utilityLayout).toContain("TeacherSurfaceGate");
  });
});
