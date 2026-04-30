import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const SIDEBAR_SHELL_PATH = resolve(process.cwd(), "components/sidebar/SidebarShell.tsx");

function readSidebarShell(): string {
  return readFileSync(SIDEBAR_SHELL_PATH, "utf8");
}

test("expanded sidebar uses a wider shell and a chat-owned new-chat action", () => {
  const source = readSidebarShell();

  assert.match(source, /w-\[264px\]/);
  assert.doesNotMatch(source, /\/\*\s*Primary nav\s*\*\/[\s\S]*?<span>\{t\("New Chat"\)\}<\/span>/);
  assert.match(source, /t\("Chat"\)|>Chat</);
  assert.match(source, /Plus size=\{15\} strokeWidth=\{2\}/);
  assert.doesNotMatch(source, /max-h-\[112px\]/);
});
