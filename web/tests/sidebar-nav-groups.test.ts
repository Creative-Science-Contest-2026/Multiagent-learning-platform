import test from "node:test";
import assert from "node:assert/strict";
import {
  getCollapsedSidebarNav,
  getExpandedSidebarGroups,
} from "../components/sidebar/nav-groups.ts";

test("expanded sidebar groups promote contest-core routes before secondary tools", () => {
  const groups = getExpandedSidebarGroups();

  assert.equal(groups.length, 2);
  assert.equal(groups[0]?.id, "contest-core");
  assert.deepEqual(
    groups[0]?.items.map((item) => item.href),
    ["/knowledge", "/dashboard", "/agents", "/marketplace"],
  );

  assert.equal(groups[1]?.id, "secondary-tools");
  assert.deepEqual(
    groups[1]?.items.map((item) => item.href),
    ["/", "/guide", "/co-writer", "/memory"],
  );
});

test("collapsed sidebar keeps only contest-core routes visible by default", () => {
  const items = getCollapsedSidebarNav();

  assert.deepEqual(items.map((item) => item.href), [
    "/knowledge",
    "/dashboard",
    "/agents",
    "/marketplace",
  ]);
  assert.equal(items.some((item) => item.href === "/co-writer"), false);
  assert.equal(items.some((item) => item.href === "/memory"), false);
});
