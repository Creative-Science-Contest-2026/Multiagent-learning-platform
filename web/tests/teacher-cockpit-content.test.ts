import { describe, expect, it } from "vitest";
import {
  getTeacherCockpitPrimaryActions,
  getTeacherCockpitSupportActions,
} from "../components/contest/teacher-cockpit-content";

describe("teacher cockpit content", () => {
  it("points primary actions to the contest setup and review flow", () => {
    const actions = getTeacherCockpitPrimaryActions();

    expect(actions.map((action) => action.href)).toEqual([
      "/knowledge",
      "/agents",
      "/dashboard",
      "/marketplace",
    ]);
  });

  it("keeps the broader workspace as a secondary support path", () => {
    const actions = getTeacherCockpitSupportActions();

    expect(actions.some((action) => action.href === "/playground")).toBe(true);
    expect(actions.some((action) => action.href === "/")).toBe(false);
  });
});
