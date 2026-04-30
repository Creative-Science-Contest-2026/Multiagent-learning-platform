import test from "node:test";
import assert from "node:assert/strict";
import {
  getTeacherCockpitPrimaryActions,
  getTeacherCockpitSupportActions,
} from "../components/contest/teacher-cockpit-content.ts";

test("teacher cockpit primary actions point to the contest setup and review flow", () => {
  const actions = getTeacherCockpitPrimaryActions();

  assert.deepEqual(
    actions.map((action) => action.href),
    ["/knowledge", "/agents", "/dashboard", "/marketplace"],
  );
});

test("teacher cockpit support actions keep the broad workspace as a secondary path", () => {
  const actions = getTeacherCockpitSupportActions();

  assert.equal(actions.some((action) => action.href === "/playground"), true);
  assert.equal(actions.some((action) => action.href === "/"), false);
});
