import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const SETTINGS_PAGE_PATH = resolve(process.cwd(), "app/(utility)/settings/page.tsx");

function readSettingsPageSource(): string {
  return readFileSync(SETTINGS_PAGE_PATH, "utf8");
}

test("settings page hides runtime service configuration from end users", () => {
  const source = readSettingsPageSource();

  assert.match(source, /t\("Settings"\)/);
  assert.match(source, /t\("Theme"\)/);
  assert.match(source, /t\("Language"\)/);

  assert.doesNotMatch(source, /service configuration/i);
  assert.doesNotMatch(source, /activeService/);
  assert.doesNotMatch(source, /serviceIcon\(/);
  assert.doesNotMatch(source, /t\("LLM"\)/);
  assert.doesNotMatch(source, /EMBEDDING/);
  assert.doesNotMatch(source, /SEARCH/);
  assert.doesNotMatch(source, /t\("Save Draft"\)/);
  assert.doesNotMatch(source, /t\("Apply"\)/);
  assert.doesNotMatch(source, /t\("Diagnostics"\)/);
  assert.doesNotMatch(source, /t\("Run test"\)/);
  assert.doesNotMatch(source, /t\("Run Terminal Tour"\)/);
  assert.doesNotMatch(source, /t\("API Key"\)/);
  assert.doesNotMatch(source, /t\("Base URL"\)/);
  assert.doesNotMatch(source, /t\("Model ID"\)/);
});
