import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import test from "node:test";

const SIDEBAR_SHELL_PATH = resolve(process.cwd(), "components/sidebar/SidebarShell.tsx");
const WORKSPACE_SIDEBAR_PATH = resolve(process.cwd(), "components/sidebar/WorkspaceSidebar.tsx");
const UTILITY_SIDEBAR_PATH = resolve(process.cwd(), "components/sidebar/UtilitySidebar.tsx");

function readSidebarShell(): string {
  return readFileSync(SIDEBAR_SHELL_PATH, "utf8");
}

function readWorkspaceSidebar(): string {
  return readFileSync(WORKSPACE_SIDEBAR_PATH, "utf8");
}

function readUtilitySidebar(): string {
  return readFileSync(UTILITY_SIDEBAR_PATH, "utf8");
}

test("expanded sidebar uses a wider shell and a chat-owned new-chat action", () => {
  const source = readSidebarShell();

  assert.match(source, /w-\[264px\]/);
  assert.doesNotMatch(source, /\/\*\s*Primary nav\s*\*\/[\s\S]*?<span>\{t\("New Chat"\)\}<\/span>/);
  assert.match(source, /t\("Chat"\)|>Chat</);
  assert.match(source, /Plus size=\{15\} strokeWidth=\{2\}/);
  assert.doesNotMatch(source, /max-h-\[112px\]/);
});

test("sidebar shell supports explicit chat and business workspace modes", () => {
  const source = readSidebarShell();

  assert.match(source, /shellMode\?: "chat" \| "business"/);
  assert.match(source, /const isChatWorkspace = shellMode === "chat"/);
  assert.match(source, /\{isChatWorkspace \? \(/);
});

test("workspace and utility sidebars wire business routes away from dominant chat history", () => {
  const workspaceSource = readWorkspaceSidebar();
  const utilitySource = readUtilitySidebar();

  assert.match(workspaceSource, /const shellMode = pathname\.startsWith\("\/playground"\) \? "chat" : "business"/);
  assert.match(workspaceSource, /shellMode=\{shellMode\}/);
  assert.match(utilitySource, /<SidebarShell shellMode="business" \/>/);
  assert.doesNotMatch(utilitySource, /listSessions|updateSessionTitle|deleteSession/);
});
