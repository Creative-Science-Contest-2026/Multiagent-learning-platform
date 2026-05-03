import { readFileSync } from "node:fs";
import path from "node:path";

import { describe, expect, it } from "vitest";

const workspaceLayout = readFileSync(path.resolve(__dirname, "../app/(workspace)/layout.tsx"), "utf-8");
const utilityLayout = readFileSync(path.resolve(__dirname, "../app/(utility)/layout.tsx"), "utf-8");
const teacherLayout = readFileSync(path.resolve(__dirname, "../app/teacher/layout.tsx"), "utf-8");
const studentLayout = readFileSync(path.resolve(__dirname, "../app/student/layout.tsx"), "utf-8");
const adminLayout = readFileSync(path.resolve(__dirname, "../app/admin/layout.tsx"), "utf-8");

describe("shared shell layouts", () => {
  it("guard the workspace shell with TeacherSurfaceGate", () => {
    expect(workspaceLayout).toContain("TeacherSurfaceGate");
  });

  it("guard the utility shell with TeacherSurfaceGate", () => {
    expect(utilityLayout).toContain("TeacherSurfaceGate");
  });

  it("render the verification banner in the teacher shell", () => {
    expect(teacherLayout).toContain("EmailVerificationBanner");
    expect(teacherLayout).toContain("SignedInAccountBar");
  });

  it("render the verification banner in the student shell", () => {
    expect(studentLayout).toContain("EmailVerificationBanner");
    expect(studentLayout).toContain("SignedInAccountBar");
  });

  it("render the verification banner in the admin shell", () => {
    expect(adminLayout).toContain("EmailVerificationBanner");
    expect(adminLayout).toContain("SignedInAccountBar");
  });
});
