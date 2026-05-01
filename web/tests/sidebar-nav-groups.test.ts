import { describe, expect, it } from "vitest";
import {
  getCollapsedSidebarNav,
  getExpandedSidebarGroups,
} from "../components/sidebar/nav-groups";

describe("sidebar nav groups", () => {
  it("promotes contest-core routes before secondary tools in the expanded sidebar", () => {
    const groups = getExpandedSidebarGroups();

    expect(groups).toHaveLength(2);
    expect(groups[0]?.id).toBe("contest-core");
    expect(groups[0]?.items.map((item) => item.href)).toEqual([
      "/knowledge",
      "/dashboard",
      "/agents",
      "/marketplace",
    ]);

    expect(groups[1]?.id).toBe("secondary-tools");
    expect(groups[1]?.items.map((item) => item.href)).toEqual([
      "/playground",
      "/memory",
    ]);
  });

  it("keeps only contest-core routes visible by default in the collapsed sidebar", () => {
    const items = getCollapsedSidebarNav();

    expect(items.map((item) => item.href)).toEqual([
      "/knowledge",
      "/dashboard",
      "/agents",
      "/marketplace",
      "/playground",
    ]);
    expect(items.some((item) => item.href === "/guide")).toBe(false);
    expect(items.some((item) => item.href === "/co-writer")).toBe(false);
    expect(items.some((item) => item.href === "/memory")).toBe(false);
  });
});
