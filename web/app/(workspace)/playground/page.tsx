"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  BrainCircuit,
  Columns3,
  ChevronDown,
  Check,
  ChevronsLeftRight,
  Code2,
  Database,
  Expand,
  FileText,
  FileSearch,
  Globe,
  Lightbulb,
  Loader2,
  MessageSquare,
  Microscope,
  PanelRightClose,
  PanelRightOpen,
  PenLine,
  Play,
  Sparkles,
  Terminal,
  Upload,
  X,
  type LucideIcon,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { apiUrl } from "@/lib/api";
import { PlaygroundRightPanel } from "@/components/chat/home/PlaygroundRightPanel";
import { PlaygroundWorkspaceShell } from "@/components/chat/home/PlaygroundWorkspaceShell";
import AssistantResponse from "@/components/common/AssistantResponse";
import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import ProcessLogs from "@/components/common/ProcessLogs";
import { useUnifiedChat, type MessageItem, type TutorPackBinding } from "@/context/UnifiedChatContext";
import ResearchConfigPanel from "@/components/research/ResearchConfigPanel";
import { extractBase64FromDataUrl, readFileAsDataUrl } from "@/lib/file-attachments";
import { listKnowledgeBases, type KnowledgeBaseSummary } from "@/lib/knowledge-api";
import type { StreamEvent } from "@/lib/unified-ws";
import { buildPlaygroundTraceRows } from "@/lib/playground-trace";
import {
  filterFrontendTools,
  FRONTEND_HIDDEN_TOOLS,
  loadCapabilityPlaygroundConfigs,
  resolveCapabilityPlaygroundConfig,
  saveCapabilityPlaygroundConfig,
  type CapabilityPlaygroundConfig,
  type CapabilityPlaygroundConfigMap,
} from "@/lib/playground-config";
import {
  buildResearchWSConfig,
  createEmptyResearchConfig,
  normalizeResearchConfig,
  validateResearchConfig,
  type DeepResearchFormConfig,
  type ResearchSource,
} from "@/lib/research-types";

/* ------------------------------------------------------------------ */
/*  Icon maps — consistent with chat page                              */
/* ------------------------------------------------------------------ */

const TOOL_ICONS: Record<string, LucideIcon> = {
  brainstorm: Lightbulb,
  rag: Database,
  web_search: Globe,
  code_execution: Code2,
  reason: Sparkles,
  paper_search: FileSearch,
};

const TOOL_LABELS: Record<string, string> = {
  brainstorm: "Brainstorm",
  rag: "RAG",
  web_search: "Web Search",
  code_execution: "Code Execution",
  reason: "Reason",
  paper_search: "Arxiv Search",
};

const RESEARCH_SOURCE_OPTIONS: Array<{ name: ResearchSource; label: string; icon: LucideIcon }> = [
  { name: "kb", label: "Knowledge Base", icon: Database },
  { name: "web", label: "Web", icon: Globe },
  { name: "papers", label: "Papers", icon: FileSearch },
];

const CAPABILITY_ICONS: Record<string, LucideIcon> = {
  chat: MessageSquare,
  deep_solve: BrainCircuit,
  deep_question: PenLine,
  deep_research: Microscope,
};

const CAPABILITY_LABELS: Record<string, string> = {
  chat: "Chat",
  deep_solve: "Deep Solve",
  deep_question: "Quiz Generation",
  deep_research: "Deep Research",
};

function getToolIcon(name: string): LucideIcon {
  return TOOL_ICONS[name] ?? Terminal;
}

function getToolLabel(name: string): string {
  return TOOL_LABELS[name] ?? titleCase(name);
}

function getCapabilityLabel(name: string): string {
  return CAPABILITY_LABELS[name] ?? titleCase(name);
}

function getToolDescription(description: string, t: (key: string) => string): string {
  return t(description);
}

function getCapabilityDescription(description: string, t: (key: string) => string): string {
  return t(description);
}

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface ToolParam {
  name: string;
  type: string;
  description?: string;
  required?: boolean;
  default?: unknown;
  enum?: string[] | null;
}

interface ToolInfo {
  name: string;
  description: string;
  parameters?: ToolParam[];
}

interface CapabilityInfo {
  name: string;
  description: string;
  stages?: string[];
  tools_used?: string[];
}

interface ExecResult {
  success: boolean;
  content: string;
  sources: Array<Record<string, string>>;
  metadata: Record<string, unknown>;
}

interface CapabilityExecResult {
  success: boolean;
  data: Record<string, unknown>;
  elapsedMs?: number;
}

interface KnowledgeBase {
  name: string;
  is_default?: boolean;
  status?: string;
  metadata?: KnowledgeBaseSummary["metadata"];
}

interface TutorPackOption {
  name: string;
  knowledgeBase: string;
  subject?: string | null;
  grade?: string | null;
  owner?: string | null;
  language?: string | null;
}

interface TesterMessage {
  role: "user" | "assistant";
  content: string;
  events?: StreamEvent[];
  processLogs?: string[];
  result?: CapabilityExecResult | null;
  error?: string | null;
}

interface PlaygroundChatMessage extends TesterMessage {
  role: "user" | "assistant";
}

type DeepQuestionMode = "custom" | "mimic";

interface DeepQuestionFormConfig {
  mode: DeepQuestionMode;
  topic: string;
  num_questions: number;
  difficulty: string;
  question_type: string;
  preference: string;
  paper_path: string;
  max_questions: number;
}

/* ------------------------------------------------------------------ */
/*  Helpers                                                            */
/* ------------------------------------------------------------------ */

function titleCase(v: string) {
  return v.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

const QUERY_PARAM_NAMES = new Set(["query", "intent", "code", "topic"]);

const DEFAULT_DEEP_QUESTION_CONFIG: DeepQuestionFormConfig = {
  mode: "custom",
  topic: "",
  num_questions: 3,
  difficulty: "auto",
  question_type: "auto",
  preference: "",
  paper_path: "",
  max_questions: 10,
};

function normalizeDeepQuestionConfig(
  raw: Record<string, unknown> | undefined,
): DeepQuestionFormConfig {
  const mode = raw?.mode === "mimic" ? "mimic" : "custom";
  return {
    mode,
    topic: typeof raw?.topic === "string" ? raw.topic : "",
    num_questions:
      typeof raw?.num_questions === "number" && raw.num_questions > 0
        ? raw.num_questions
        : DEFAULT_DEEP_QUESTION_CONFIG.num_questions,
    difficulty:
      typeof raw?.difficulty === "string" && raw.difficulty
        ? raw.difficulty
        : DEFAULT_DEEP_QUESTION_CONFIG.difficulty,
    question_type:
      typeof raw?.question_type === "string" && raw.question_type
        ? raw.question_type
        : DEFAULT_DEEP_QUESTION_CONFIG.question_type,
    preference: typeof raw?.preference === "string" ? raw.preference : "",
    paper_path: typeof raw?.paper_path === "string" ? raw.paper_path : "",
    max_questions:
      typeof raw?.max_questions === "number" && raw.max_questions > 0
        ? raw.max_questions
        : DEFAULT_DEEP_QUESTION_CONFIG.max_questions,
  };
}

/* ------------------------------------------------------------------ */
/*  TracePanel                                                         */
/* ------------------------------------------------------------------ */

function TracePanel({ events }: { events: StreamEvent[] }) {
  const { t } = useTranslation();
  if (!events.length) return null;

  const grouped = new Map<string, StreamEvent[]>();
  for (const ev of events) {
    const key = ev.stage || "session";
    const list = grouped.get(key) ?? [];
    list.push(ev);
    grouped.set(key, list);
  }

  return (
    <div className="space-y-1.5">
      {Array.from(grouped.entries()).map(([stage, stageEvents]) => {
        const renderable = stageEvents.filter((e) =>
          ["thinking", "progress", "tool_call", "tool_result", "error"].includes(e.type),
        );
        const rows = buildPlaygroundTraceRows(renderable);
        if (!rows.length) return null;
        return (
          <details key={stage} className="group rounded-2xl">
            <summary className="flex cursor-pointer list-none items-center gap-2 py-1 text-[12px] font-medium text-[var(--muted-foreground)] transition-colors hover:text-[var(--foreground)] [&::-webkit-details-marker]:hidden">
              <ChevronDown
                size={12}
                className="shrink-0 text-[var(--muted-foreground)] transition-transform group-open:rotate-180"
              />
              <span className="inline-flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-[var(--muted-foreground)]/40" />
                {stage === "session" ? t("Details") : t(titleCase(stage))}
              </span>
            </summary>
            <div className="ml-3 space-y-1.5 border-l border-[var(--border)]/35 pl-4">
              {rows.map((row, i) => {
                if (row.type === "thinking") return <p key={`${stage}-t-${i}`} className="text-[12px] italic leading-relaxed text-[var(--muted-foreground)]/88">{row.content}</p>;
                if (row.type === "progress") {
                  const cur = Number(row.event.metadata?.current ?? 0), tot = Number(row.event.metadata?.total ?? 0);
                  return (
                    <div key={`${stage}-p-${i}`} className="rounded-2xl bg-[var(--muted)]/38 px-3 py-2 text-[12px] text-[var(--muted-foreground)]">
                      <div>{row.content}</div>
                      {tot > 0 && <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-[var(--border)]"><div className="h-full rounded-full bg-[var(--primary)] transition-all duration-300" style={{ width: `${Math.min(100, (cur / tot) * 100)}%` }} /></div>}
                    </div>
                  );
                }
                if (row.type === "tool_call" || row.type === "tool_result") return (
                  <div key={`${stage}-tc-${i}`} className="rounded-2xl border border-[var(--border)]/40 bg-[var(--background)]/66 px-3 py-2">
                    <div className="text-[10px] uppercase tracking-[0.14em] text-[var(--muted-foreground)]/82">{row.type === "tool_call" ? t("Tool call") : t("Tool result")}</div>
                    <div className="mt-1 text-[12px] leading-5 text-[var(--foreground)]/88">{row.content || String(row.event.metadata?.tool ?? "")}</div>
                  </div>
                );
                if (row.type === "error") return <div key={`${stage}-e-${i}`} className="rounded-2xl border border-red-200/60 bg-red-50/72 px-3 py-2 text-[12px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">{row.content}</div>;
                return null;
              })}
            </div>
          </details>
        );
      })}
    </div>
  );
}

function getResultResponse(result: CapabilityExecResult | null | undefined): string {
  return typeof result?.data.response === "string" ? result.data.response.trim() : "";
}

function toPlaygroundChatMessages(messages: MessageItem[]): PlaygroundChatMessage[] {
  return messages.flatMap((message) => {
    if (message.role === "system") return [];
    const errorEvent = message.events?.find((event) => event.type === "error");
    return [
      {
        role: message.role,
        content: message.content,
        events: message.events ?? [],
        result: null,
        processLogs: [],
        error: errorEvent?.content || null,
      },
    ];
  });
}

function PlaygroundChatTurn({
  msg,
  isStreaming,
  isLatestAssistant,
}: {
  msg: TesterMessage;
  isStreaming: boolean;
  isLatestAssistant: boolean;
}) {
  const { t } = useTranslation();
  const resultResponse = getResultResponse(msg.result);
  const displayedContent = msg.content.trim();
  const shouldRenderAssistantContent = Boolean(displayedContent);
  const shouldRenderCapabilityResult =
    Boolean(msg.result) &&
    ((!resultResponse && Object.keys(msg.result?.data ?? {}).length > 0) ||
      (resultResponse && resultResponse !== displayedContent));

  return (
    <div className={`mx-auto max-w-4xl ${msg.role === "user" ? "flex justify-end" : ""}`}>
      <div className={msg.role === "user" ? "w-full max-w-[min(42rem,64%)]" : "w-full max-w-[82%]"}>
        <div className="mb-2 flex items-center gap-2 text-[10px] uppercase tracking-[0.14em] text-[var(--muted-foreground)]">
          {msg.role === "user" ? <MessageSquare size={12} /> : <Sparkles size={12} />}
          <span>{msg.role === "user" ? t("You") : t("Assistant")}</span>
        </div>
        {msg.role === "user" ? (
          <div className="rounded-[22px] border border-[var(--border)]/45 bg-[var(--muted)]/78 px-4 py-3 text-[15px] leading-7 text-[var(--foreground)] shadow-[0_10px_28px_rgba(15,23,42,0.04)]">
            {msg.content}
          </div>
        ) : (
          <div className="space-y-3">
            {(msg.events || []).length > 0 ? (
              <div className="mb-1">
                <TracePanel events={msg.events || []} />
              </div>
            ) : null}
            {msg.error && (
              <div className="rounded-[18px] border border-red-200/70 bg-red-50/80 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
                {msg.error}
              </div>
            )}
            {shouldRenderAssistantContent ? (
              <AssistantResponse
                content={msg.content}
                className="rounded-[22px] border border-[var(--border)]/38 bg-[var(--background)]/70 px-5 py-4 shadow-[0_8px_24px_rgba(15,23,42,0.03)]"
              />
            ) : null}
            {shouldRenderCapabilityResult ? (
              <CapabilityResultPanel result={msg.result} streamedContent={msg.content} />
            ) : null}
            {!msg.error && isStreaming && isLatestAssistant && !shouldRenderAssistantContent ? (
              <div className="inline-flex items-center gap-2 rounded-full bg-[var(--muted)]/55 px-3 py-1.5 text-[12px] text-[var(--muted-foreground)]">
                <Loader2 size={12} className="animate-spin" />
                {t("Running...")}
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
}

function PlaygroundSharedChat({
  messages,
  isStreaming,
  title,
  onSend,
  onCancel,
  disabled,
  disabledReason,
}: {
  messages: MessageItem[];
  isStreaming: boolean;
  title: string;
  onSend: (content: string) => void;
  onCancel: () => void;
  disabled?: boolean;
  disabledReason?: string | null;
}) {
  const { t } = useTranslation();
  const [input, setInput] = useState("");
  const chatMessages = useMemo(() => toPlaygroundChatMessages(messages), [messages]);

  const send = () => {
    const content = input.trim();
    if (!content || isStreaming || disabled) return;
    onSend(content);
    setInput("");
  };

  return (
    <div className="flex h-full min-h-0 flex-col gap-4">
      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="space-y-5 pb-4">
          {chatMessages.map((msg, i) => (
            <PlaygroundChatTurn
              key={`${msg.role}-${i}`}
              msg={msg}
              isStreaming={isStreaming}
              isLatestAssistant={i === chatMessages.length - 1}
            />
          ))}
        </div>
      </div>
      <div className="sticky bottom-0 z-10 shrink-0 border-t border-[var(--border)] bg-[var(--background)]/96 pt-2 backdrop-blur">
        <div className="rounded-[22px] border border-[var(--border)]/60 bg-[var(--background)]/84 px-3 py-2.5 shadow-[0_1px_2px_rgba(15,23,42,0.03)]">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (isStreaming) onCancel();
                else if (!disabled) send();
              }
            }}
            rows={2}
            placeholder={`${t("Try")} ${title}...`}
            disabled={disabled}
            className="w-full resize-none bg-transparent text-[13px] leading-5 text-[var(--foreground)] outline-none placeholder:text-[var(--muted-foreground)] disabled:cursor-not-allowed disabled:opacity-50"
          />
          <div className="mt-2 flex items-center justify-between gap-3">
            <div className="text-[11px] text-[var(--muted-foreground)]">
              {disabled && disabledReason
                ? disabledReason
                : isStreaming
                ? t("Press Enter to stop the current answer.")
                : t("Enter to send, Shift+Enter for a new line.")}
            </div>
            <button
              onClick={isStreaming ? onCancel : send}
              disabled={disabled || (!isStreaming && !input.trim())}
              className="inline-flex items-center gap-2 rounded-full bg-[var(--muted)] px-4 py-1.5 text-[12px] font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/80 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {isStreaming ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
              {isStreaming ? t("Stop") : t("Send")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  ToolExecutor                                                       */
/* ------------------------------------------------------------------ */

function ToolExecutor({ tool, knowledgeBases }: { tool: ToolInfo; knowledgeBases: KnowledgeBase[] }) {
  const { t } = useTranslation();
  const params = tool.parameters ?? [];
  const [values, setValues] = useState<Record<string, string>>({});
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<ExecResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [processLogs, setProcessLogs] = useState<string[]>([]);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    setValues({});
    setResult(null);
    setError(null);
    setProcessLogs([]);
  }, [tool.name]);

  useEffect(() => () => { abortRef.current?.abort(); }, []);

  const setParam = (name: string, val: string) => setValues((p) => ({ ...p, [name]: val }));

  const queryParam = params.find((p) => QUERY_PARAM_NAMES.has(p.name));
  const otherParams = params.filter((p) => !QUERY_PARAM_NAMES.has(p.name));

  const execute = async () => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    setExecuting(true);
    setResult(null);
    setError(null);
    setProcessLogs([]);
    try {
      const coerced: Record<string, unknown> = {};
      for (const p of params) {
        const raw = values[p.name];
        if (!raw) continue;
        if (p.type === "integer") coerced[p.name] = parseInt(raw, 10);
        else if (p.type === "number") coerced[p.name] = parseFloat(raw);
        else if (p.type === "boolean") coerced[p.name] = raw === "true";
        else coerced[p.name] = raw;
      }

      const res = await fetch(apiUrl(`/api/v1/plugins/tools/${tool.name}/execute-stream`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ params: coerced }),
        signal: controller.signal,
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || `HTTP ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          if (!part.trim()) continue;
          const eventMatch = part.match(/^event:\s*(.+)$/m);
          const dataMatch = part.match(/^data:\s*(.+)$/m);
          if (!eventMatch || !dataMatch) continue;

          const eventType = eventMatch[1].trim();
          let payload: Record<string, unknown>;
          try { payload = JSON.parse(dataMatch[1]); } catch { continue; }

          if (eventType === "log") {
            const line = (payload.line as string) ?? "";
            setProcessLogs((prev) => [...prev, line]);
          } else if (eventType === "result") {
            setResult({
              success: payload.success as boolean,
              content: (payload.content as string) ?? "",
              sources: (payload.sources as Array<Record<string, string>>) ?? [],
              metadata: (payload.metadata as Record<string, unknown>) ?? {},
            });
          } else if (eventType === "error") {
            setError((payload.detail as string) ?? "Unknown error");
          }
        }
      }
    } catch (err: unknown) {
      if (controller.signal.aborted) return;
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      if (!controller.signal.aborted) setExecuting(false);
    }
  };

  const isKbNameParam = (p: ToolParam) => p.name === "kb_name";

  const renderParam = (p: ToolParam) => {
    if (isKbNameParam(p)) {
      return (
        <select
          value={values[p.name] ?? ""}
          onChange={(e) => setParam(p.name, e.target.value)}
          className="w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
        >
          <option value="">{t("Select knowledge base...")}</option>
          {knowledgeBases.map((kb) => <option key={kb.name} value={kb.name}>{kb.name}{kb.is_default ? ` (${t("default")})` : ""}</option>)}
        </select>
      );
    }

    if (p.enum) {
      return (
        <select
          value={values[p.name] ?? ""}
          onChange={(e) => setParam(p.name, e.target.value)}
          className="w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
        >
          <option value="">{t("Select...")}</option>
          {p.enum.map((v) => <option key={v} value={v}>{v}</option>)}
        </select>
      );
    }

    return (
      <input
        type={p.type === "integer" || p.type === "number" ? "number" : "text"}
        value={values[p.name] ?? ""}
        onChange={(e) => setParam(p.name, e.target.value)}
        placeholder={p.description || p.name}
        className="w-full rounded-lg border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
      />
    );
  };

  return (
    <div className="space-y-5">
      {/* Config params (non-query) */}
      {otherParams.length > 0 && (
        <div>
          <h4 className="mb-2.5 text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">{t("Parameters")}</h4>
          <div className="grid gap-3 md:grid-cols-2">
            {otherParams.map((p) => (
              <div key={`${tool.name}-${p.name}`}>
                <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {p.name}
                  {p.required !== false && <span className="ml-0.5 text-[var(--primary)]">*</span>}
                  <span className="ml-1.5 text-[10px] font-normal uppercase text-[var(--muted-foreground)]">{p.type}</span>
                </label>
                {renderParam(p)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Query input — visually distinct */}
      {queryParam && (
        <div className="rounded-xl border-2 border-dashed border-[var(--primary)]/30 bg-[var(--primary)]/[0.03] p-4">
          <label className="mb-2 flex items-center gap-1.5 text-[12px] font-semibold text-[var(--primary)]">
            <Terminal size={13} />
            {queryParam.name === "code" ? t("Code input") : t("Query input")}
          </label>
          {queryParam.name === "code" || queryParam.name === "topic" ? (
            <textarea
              value={values[queryParam.name] ?? ""}
              onChange={(e) => setParam(queryParam.name, e.target.value)}
              placeholder={queryParam.description || t("Enter your input...")}
              rows={queryParam.name === "topic" ? 5 : 4}
              className="w-full resize-none rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2.5 font-mono text-[13px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
            />
          ) : (
            <input
              type="text"
              value={values[queryParam.name] ?? ""}
              onChange={(e) => setParam(queryParam.name, e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !executing) execute(); }}
              placeholder={queryParam.description || t("Enter your query...")}
              className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2.5 text-[14px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
            />
          )}
        </div>
      )}

      {/* Execute button */}
      <button
        onClick={execute}
        disabled={executing}
        className="inline-flex items-center gap-1.5 rounded-lg bg-[var(--primary)] px-4 py-2 text-[13px] font-medium text-[var(--primary-foreground)] transition-opacity disabled:opacity-50"
      >
        {executing ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
        {executing ? t("Running...") : t("Execute")}
      </button>

      {/* Process Logs */}
      <ProcessLogs logs={processLogs} executing={executing} />

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-[13px] text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            {result.success ? (
              <span className="inline-flex items-center gap-1 rounded-md bg-green-50 px-2 py-0.5 text-[11px] font-medium text-green-700 dark:bg-green-950/30 dark:text-green-400">
                <Check size={10} /> {t("Success")}
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 rounded-md bg-red-50 px-2 py-0.5 text-[11px] font-medium text-red-700 dark:bg-red-950/30 dark:text-red-400">
                <X size={10} /> {t("Failed")}
              </span>
            )}
          </div>

          {result.content && (
            <div className="max-h-[400px] overflow-y-auto rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
              <MarkdownRenderer content={result.content} variant="prose" />
            </div>
          )}

          {result.sources.length > 0 && (
            <details className="group rounded-lg border border-[var(--border)] bg-[var(--card)]">
              <summary className="flex cursor-pointer list-none items-center justify-between px-3 py-2 text-[13px] font-medium text-[var(--foreground)]">
                {t("Sources")} ({result.sources.length})
                <ChevronDown size={13} className="text-[var(--muted-foreground)] transition-transform group-open:rotate-180" />
              </summary>
              <div className="border-t border-[var(--border)] px-3 py-2.5 space-y-1.5">
                {result.sources.map((s, i) => (
                  <div key={`src-${i}`} className="rounded-md bg-[var(--muted)] px-2.5 py-1.5 text-[12px]">
                    <div className="font-medium text-[var(--foreground)]">{s.title || s.query || s.type || t("Source")}</div>
                    {s.url && <div className="mt-0.5 break-all text-[11px] text-[var(--muted-foreground)]">{s.url}</div>}
                  </div>
                ))}
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  CapabilityResultPanel                                              */
/* ------------------------------------------------------------------ */

function CapabilityResultPanel({
  result,
  streamedContent = "",
}: {
  result: CapabilityExecResult | null | undefined;
  streamedContent?: string;
}) {
  const { t } = useTranslation();
  if (!result) return null;

  const response = getResultResponse(result);
  const normalizedStreamedContent = streamedContent.trim();
  const shouldRenderResponse = Boolean(response) && response !== normalizedStreamedContent;
  const extraData = Object.fromEntries(
    Object.entries(result.data).filter(([key]) => key !== "response"),
  );
  const extraKeys = Object.keys(extraData);
  const shouldRenderStructuredFallback = !response && extraKeys.length > 0;
  const shouldRenderStatus =
    !result.success ||
    (!shouldRenderResponse && !shouldRenderStructuredFallback && !normalizedStreamedContent);

  if (!shouldRenderResponse && !shouldRenderStructuredFallback && !shouldRenderStatus) {
    return null;
  }

  return (
    <div className="space-y-2">
      {shouldRenderStatus ? (
        <div className="flex items-center gap-2 text-[11px] text-[var(--muted-foreground)]">
          {!result.success ? (
            <span className="inline-flex items-center gap-1 rounded-full bg-red-50 px-2 py-0.5 text-red-700 dark:bg-red-950/30 dark:text-red-300">
              <X size={10} /> {t("Failed")}
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-0.5 text-green-700 dark:bg-green-950/30 dark:text-green-400">
              <Check size={10} /> {t("Success")}
            </span>
          )}
          {typeof result.elapsedMs === "number" ? (
            <span>
              {result.elapsedMs} {t("ms")}
            </span>
          ) : null}
        </div>
      ) : null}

      {shouldRenderResponse ? (
        <AssistantResponse
          content={response}
          className="rounded-[22px] border border-[var(--border)]/38 bg-[var(--background)]/66 px-5 py-4 shadow-[0_8px_24px_rgba(15,23,42,0.03)]"
        />
      ) : null}

      {shouldRenderStructuredFallback ? (
        <div className="rounded-[20px] border border-[var(--border)]/45 bg-[var(--background)]/64 p-3">
          <pre className="overflow-x-auto whitespace-pre-wrap break-all text-[12px] leading-6 text-[var(--muted-foreground)]/90">
            {JSON.stringify(extraData, null, 2)}
          </pre>
        </div>
      ) : null}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  DeepQuestionTester                                                 */
/* ------------------------------------------------------------------ */

function DeepQuestionTester({
  capability,
  enabledTools,
  knowledgeBase,
  config,
  onConfigChange,
}: {
  capability: CapabilityInfo;
  enabledTools: string[];
  knowledgeBase: string;
  config: DeepQuestionFormConfig;
  onConfigChange: (next: DeepQuestionFormConfig) => void;
}) {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState<TesterMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [uploadedPdf, setUploadedPdf] = useState<File | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => { abortRef.current?.abort(); }, []);

  const updateLastAssistant = (updater: (msg: TesterMessage) => TesterMessage) => {
    setMessages((prev) => {
      const msgs = [...prev];
      const last = msgs[msgs.length - 1];
      if (last?.role !== "assistant") return prev;
      msgs[msgs.length - 1] = updater(last);
      return msgs;
    });
  };

  const updateConfig = <K extends keyof DeepQuestionFormConfig>(
    key: K,
    value: DeepQuestionFormConfig[K],
  ) => {
    onConfigChange({ ...config, [key]: value });
  };

  const fileToAttachment = async (file: File) => {
    const dataUrl = await readFileAsDataUrl(file);
    return {
      type: "pdf",
      filename: file.name,
      mime_type: file.type || "application/pdf",
      base64: extractBase64FromDataUrl(dataUrl),
    };
  };

  const canRun =
    config.mode === "custom"
      ? config.topic.trim().length > 0
      : Boolean(uploadedPdf) || config.paper_path.trim().length > 0;

  const run = async () => {
    if (!canRun || streaming) return;

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const userContent =
      config.mode === "custom"
        ? config.topic.trim()
        : uploadedPdf
          ? t("Mimic questions from uploaded paper: {{name}}", { name: uploadedPdf.name })
          : t("Mimic questions from parsed paper: {{name}}", {
              name: config.paper_path.trim(),
            });

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userContent },
      { role: "assistant", content: "", events: [], processLogs: [], result: null, error: null },
    ]);
    setStreaming(true);

    try {
      const attachments =
        config.mode === "mimic" && uploadedPdf ? [await fileToAttachment(uploadedPdf)] : [];

      const requestConfig =
        config.mode === "custom"
          ? {
              mode: "custom",
              topic: config.topic.trim(),
              num_questions: config.num_questions,
              difficulty: config.difficulty === "auto" ? "" : config.difficulty,
              question_type: config.question_type === "auto" ? "" : config.question_type,
              preference: config.preference.trim(),
            }
          : {
              mode: "mimic",
              paper_path: uploadedPdf ? "" : config.paper_path.trim(),
              max_questions: config.max_questions,
            };

      const res = await fetch(
        apiUrl(`/api/v1/plugins/capabilities/${capability.name}/execute-stream`),
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content: userContent,
            tools: enabledTools,
            knowledge_bases: enabledTools.includes("rag") && knowledgeBase ? [knowledgeBase] : [],
            language: i18n.language,
            config: requestConfig,
            attachments,
          }),
          signal: controller.signal,
        },
      );

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || `HTTP ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          if (!part.trim()) continue;
          const eventMatch = part.match(/^event:\s*(.+)$/m);
          const dataMatch = part.match(/^data:\s*(.+)$/m);
          if (!eventMatch || !dataMatch) continue;

          const eventType = eventMatch[1].trim();
          let payload: Record<string, unknown>;
          try {
            payload = JSON.parse(dataMatch[1]);
          } catch {
            continue;
          }

          if (eventType === "log") {
            const line = (payload.line as string) ?? "";
            updateLastAssistant((last) => ({
              ...last,
              processLogs: [...(last.processLogs || []), line],
            }));
            continue;
          }

          if (eventType === "stream") {
            const event = payload as unknown as StreamEvent;
            if (event.type === "session" || event.type === "done") continue;
            updateLastAssistant((last) => ({
              ...last,
              content: event.type === "content" ? `${last.content}${event.content}` : last.content,
              events: [...(last.events || []), event],
            }));
            continue;
          }

          if (eventType === "result") {
            updateLastAssistant((last) => ({
              ...last,
              result: {
                success: Boolean(payload.success),
                data: ((payload.data as Record<string, unknown>) ?? {}),
                elapsedMs: typeof payload.elapsed_ms === "number" ? payload.elapsed_ms : undefined,
              },
            }));
            continue;
          }

          if (eventType === "error") {
            updateLastAssistant((last) => ({
              ...last,
              error: (payload.detail as string) ?? "Unknown error",
            }));
          }
        }
      }
    } catch (err: unknown) {
      if (controller.signal.aborted) return;
      updateLastAssistant((last) => ({
        ...last,
        error: err instanceof Error ? err.message : String(err),
      }));
    } finally {
      if (!controller.signal.aborted) setStreaming(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-[var(--border)] bg-[var(--background)] p-4">
        <div className="mb-3 flex flex-wrap gap-2">
          <button
            onClick={() => updateConfig("mode", "custom")}
            className={`rounded-lg px-3 py-1.5 text-[12px] font-medium transition-colors ${
              config.mode === "custom"
                ? "bg-[var(--primary)]/10 text-[var(--primary)]"
                : "bg-[var(--muted)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
            }`}
          >
            {t("Custom")}
          </button>
          <button
            onClick={() => updateConfig("mode", "mimic")}
            className={`rounded-lg px-3 py-1.5 text-[12px] font-medium transition-colors ${
              config.mode === "mimic"
                ? "bg-[var(--primary)]/10 text-[var(--primary)]"
                : "bg-[var(--muted)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
            }`}
          >
            {t("Mimic Exam")}
          </button>
        </div>

        {config.mode === "custom" ? (
          <div className="space-y-3">
            <div>
              <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Topic")}
              </label>
              <textarea
                value={config.topic}
                onChange={(e) => updateConfig("topic", e.target.value)}
                rows={3}
                placeholder={t("e.g. Gradient Descent Optimization")}
                className="w-full resize-none rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2.5 text-[13px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
              />
            </div>
            <div className="grid gap-3 md:grid-cols-3">
              <div>
                <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Count")}
                </label>
                <input
                  type="number"
                  min={1}
                  max={50}
                  value={config.num_questions}
                  onChange={(e) => updateConfig("num_questions", Math.max(1, Number(e.target.value) || 1))}
                  className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
                />
              </div>
              <div>
                <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Difficulty")}
                </label>
                <select
                  value={config.difficulty}
                  onChange={(e) => updateConfig("difficulty", e.target.value)}
                  className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
                >
                  <option value="auto">{t("Auto")}</option>
                  <option value="easy">{t("Easy")}</option>
                  <option value="medium">{t("Medium")}</option>
                  <option value="hard">{t("Hard")}</option>
                </select>
              </div>
              <div>
                <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                  {t("Type")}
                </label>
                <select
                  value={config.question_type}
                  onChange={(e) => updateConfig("question_type", e.target.value)}
                  className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
                >
                  <option value="auto">{t("Auto")}</option>
                  <option value="choice">{t("Multiple Choice")}</option>
                  <option value="written">{t("Written")}</option>
                  <option value="coding">{t("Coding")}</option>
                </select>
              </div>
            </div>
            <div>
              <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Preference")}
              </label>
              <textarea
                value={config.preference}
                onChange={(e) => updateConfig("preference", e.target.value)}
                rows={3}
                placeholder={t("Extra constraints, style, focus areas...")}
                className="w-full resize-none rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2.5 text-[13px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
              />
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <div>
              <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Upload Exam Paper (PDF)")}
              </label>
              <label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl border-2 border-dashed border-[var(--border)] bg-[var(--card)] px-4 py-6 text-[13px] text-[var(--muted-foreground)] transition-colors hover:border-[var(--primary)]/40 hover:text-[var(--foreground)]">
                <Upload size={16} />
                <span>{uploadedPdf ? uploadedPdf.name : t("Click to upload PDF")}</span>
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0] ?? null;
                    setUploadedPdf(file);
                    if (file) updateConfig("paper_path", "");
                  }}
                />
              </label>
            </div>
            <div className="text-center text-[11px] uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
              {t("Or")}
            </div>
            <div>
              <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Pre-parsed Directory")}
              </label>
              <div className="relative">
                <FileText size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted-foreground)]" />
                <input
                  type="text"
                  value={config.paper_path}
                  onChange={(e) => {
                    setUploadedPdf(null);
                    updateConfig("paper_path", e.target.value);
                  }}
                  placeholder={t("e.g. 2211asm1")}
                  className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] py-2 pl-9 pr-3 text-[13px] text-[var(--foreground)] outline-none transition-colors focus:border-[var(--primary)]/40 placeholder:text-[var(--muted-foreground)]"
                />
              </div>
            </div>
            <div className="max-w-xs">
              <label className="mb-1 block text-[12px] font-medium text-[var(--foreground)]">
                {t("Max Questions")}
              </label>
              <input
                type="number"
                min={1}
                max={100}
                value={config.max_questions}
                onChange={(e) => updateConfig("max_questions", Math.max(1, Number(e.target.value) || 1))}
                className="w-full rounded-lg border border-[var(--border)] bg-[var(--card)] px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
              />
            </div>
          </div>
        )}
      </div>

      {messages.map((msg, i) => (
        <PlaygroundChatTurn
          key={`${msg.role}-${i}`}
          msg={msg}
          isStreaming={streaming}
          isLatestAssistant={i === messages.length - 1}
        />
      ))}

      <div className="sticky bottom-0 z-10 -mx-2 border-t border-[var(--border)] bg-[var(--background)]/94 px-2 pb-2 pt-2 backdrop-blur">
        <div className="mx-auto flex max-w-4xl items-center justify-between gap-3 rounded-[22px] border border-[var(--border)]/60 bg-[var(--background)]/86 px-3 py-2 shadow-[0_1px_2px_rgba(15,23,42,0.03)]">
          <div className="text-[11px] text-[var(--muted-foreground)]">
            {t("Review the setup above, then run generation.")}
          </div>
          <button
            onClick={run}
            disabled={!canRun || streaming}
            className="inline-flex items-center gap-2 rounded-full bg-[var(--muted)] px-4 py-1.5 text-[12px] font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/80 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {streaming ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
            {streaming ? t("Running...") : t("Generate")}
          </button>
        </div>
      </div>
    </div>
  );
}

function DeepResearchTester({
  capability,
  enabledTools,
  knowledgeBase,
  config,
  onConfigChange,
}: {
  capability: CapabilityInfo;
  enabledTools: string[];
  knowledgeBase: string;
  config: DeepResearchFormConfig;
  onConfigChange: (next: DeepResearchFormConfig) => void;
}) {
  const { t, i18n } = useTranslation();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<TesterMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const validation = useMemo(() => validateResearchConfig(config), [config]);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => { abortRef.current?.abort(); }, []);

  const updateLastAssistant = (updater: (msg: TesterMessage) => TesterMessage) => {
    setMessages((prev) => {
      const msgs = [...prev];
      const last = msgs[msgs.length - 1];
      if (last?.role !== "assistant") return prev;
      msgs[msgs.length - 1] = updater(last);
      return msgs;
    });
  };

  const run = async () => {
    const content = input.trim();
    if (!content || streaming || !validation.valid) return;

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setMessages((prev) => [
      ...prev,
      { role: "user", content },
      { role: "assistant", content: "", events: [], processLogs: [], result: null, error: null },
    ]);
    setStreaming(true);

    try {
      const res = await fetch(
        apiUrl(`/api/v1/plugins/capabilities/${capability.name}/execute-stream`),
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content,
            tools: enabledTools,
            knowledge_bases: config.sources.includes("kb") && knowledgeBase ? [knowledgeBase] : [],
            language: i18n.language,
            config: buildResearchWSConfig(config),
          }),
          signal: controller.signal,
        },
      );

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || `HTTP ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          if (!part.trim()) continue;
          const eventMatch = part.match(/^event:\s*(.+)$/m);
          const dataMatch = part.match(/^data:\s*(.+)$/m);
          if (!eventMatch || !dataMatch) continue;

          const eventType = eventMatch[1].trim();
          let payload: Record<string, unknown>;
          try {
            payload = JSON.parse(dataMatch[1]);
          } catch {
            continue;
          }

          if (eventType === "log") {
            const line = (payload.line as string) ?? "";
            updateLastAssistant((last) => ({
              ...last,
              processLogs: [...(last.processLogs || []), line],
            }));
            continue;
          }

          if (eventType === "stream") {
            const event = payload as unknown as StreamEvent;
            if (event.type === "session" || event.type === "done") continue;
            updateLastAssistant((last) => ({
              ...last,
              content: event.type === "content" ? `${last.content}${event.content}` : last.content,
              events: [...(last.events || []), event],
            }));
            continue;
          }

          if (eventType === "result") {
            updateLastAssistant((last) => ({
              ...last,
              result: {
                success: Boolean(payload.success),
                data: ((payload.data as Record<string, unknown>) ?? {}),
                elapsedMs: typeof payload.elapsed_ms === "number" ? payload.elapsed_ms : undefined,
              },
            }));
            continue;
          }

          if (eventType === "error") {
            updateLastAssistant((last) => ({
              ...last,
              error: (payload.detail as string) ?? "Unknown error",
            }));
          }
        }
      }
    } catch (err: unknown) {
      if (controller.signal.aborted) return;
      updateLastAssistant((last) => ({
        ...last,
        error: err instanceof Error ? err.message : String(err),
      }));
    } finally {
      if (!controller.signal.aborted) setStreaming(false);
    }
  };

  const toggleSource = (source: ResearchSource) => {
    onConfigChange({
      ...config,
      sources: config.sources.includes(source)
        ? config.sources.filter((item) => item !== source)
        : [...config.sources, source],
    });
  };

  return (
    <div className="flex h-full min-h-0 flex-col gap-4">
      <div className="shrink-0 space-y-4">
        <ResearchConfigPanel
          value={config}
          errors={validation.errors}
          collapsed={false}
          onChange={onConfigChange}
          onToggleCollapsed={() => {}}
        />
        <div className="rounded-xl border border-[var(--border)] bg-[var(--background)] p-3">
          <div className="mb-2 text-[12px] font-medium text-[var(--foreground)]">{t("Sources")}</div>
          <div className="flex flex-wrap gap-2">
            {RESEARCH_SOURCE_OPTIONS.map((source) => {
              const active = config.sources.includes(source.name);
              const Icon = source.icon;
              return (
                <button
                  key={source.name}
                  type="button"
                  onClick={() => toggleSource(source.name)}
                  className={`inline-flex h-[32px] items-center gap-1.5 rounded-full px-3 text-[12px] font-medium transition-[background-color,color,box-shadow] ${
                    active
                      ? "bg-[var(--muted)] text-[var(--foreground)] shadow-[0_1px_2px_rgba(15,23,42,0.05)] ring-1 ring-[var(--border)]/55"
                      : "text-[var(--muted-foreground)]/75 hover:bg-[var(--muted)]/55 hover:text-[var(--foreground)]"
                  }`}
                >
                  <Icon size={13} strokeWidth={1.7} />
                  {t(source.label)}
                </button>
              );
            })}
          </div>
          <div className="mt-2 text-[11px] text-[var(--muted-foreground)]">
            {config.sources.length
              ? t("Selected sources will be queried during research.")
              : t("No source selected: the run will use llm-only research.")}
          </div>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="space-y-5 pb-4">
          {messages.map((msg, i) => (
            <PlaygroundChatTurn
              key={`${msg.role}-${i}`}
              msg={msg}
              isStreaming={streaming}
              isLatestAssistant={i === messages.length - 1}
            />
          ))}
        </div>
      </div>

      <div className="sticky bottom-0 z-10 shrink-0 border-t border-[var(--border)] bg-[var(--background)]/96 pt-2 backdrop-blur">
        <div className="rounded-[22px] border border-[var(--border)]/60 bg-[var(--background)]/84 px-3 py-2.5 shadow-[0_1px_2px_rgba(15,23,42,0.03)]">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); run(); } }}
            rows={2}
            placeholder={t("Describe the research topic...")}
            className="w-full resize-none bg-transparent text-[13px] leading-5 text-[var(--foreground)] outline-none placeholder:text-[var(--muted-foreground)]"
          />
          <div className="mt-2 flex items-center justify-between gap-3">
            <div className="text-[11px] text-[var(--muted-foreground)]">
              {t("Enter to run, Shift+Enter for a new line.")}
            </div>
            <button
              onClick={run}
              disabled={!input.trim() || streaming || !validation.valid}
              className="inline-flex items-center gap-2 rounded-full bg-[var(--muted)] px-4 py-1.5 text-[12px] font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/80 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {streaming ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
              {streaming ? t("Running...") : t("Run Research")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  CapabilityTester                                                   */
/* ------------------------------------------------------------------ */

function CapabilityTester({
  capability,
  enabledTools,
  knowledgeBase,
}: {
  capability: CapabilityInfo;
  enabledTools: string[];
  knowledgeBase: string;
}) {
  const { t, i18n } = useTranslation();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<TesterMessage[]>([]);
  const [streaming, setStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => { abortRef.current?.abort(); }, []);

  const updateLastAssistant = (updater: (msg: TesterMessage) => TesterMessage) => {
    setMessages((prev) => {
      const msgs = [...prev];
      const last = msgs[msgs.length - 1];
      if (last?.role !== "assistant") return prev;
      msgs[msgs.length - 1] = updater(last);
      return msgs;
    });
  };

  const send = async () => {
    const content = input.trim();
    if (!content || streaming) return;

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setMessages((prev) => [
      ...prev,
      { role: "user", content },
      { role: "assistant", content: "", events: [], processLogs: [], result: null, error: null },
    ]);
    setInput("");
    setStreaming(true);

    try {
      const res = await fetch(
        apiUrl(`/api/v1/plugins/capabilities/${capability.name}/execute-stream`),
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content,
            tools: enabledTools,
            knowledge_bases: enabledTools.includes("rag") && knowledgeBase ? [knowledgeBase] : [],
            language: i18n.language,
          }),
          signal: controller.signal,
        },
      );

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail || `HTTP ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          if (!part.trim()) continue;
          const eventMatch = part.match(/^event:\s*(.+)$/m);
          const dataMatch = part.match(/^data:\s*(.+)$/m);
          if (!eventMatch || !dataMatch) continue;

          const eventType = eventMatch[1].trim();
          let payload: Record<string, unknown>;
          try {
            payload = JSON.parse(dataMatch[1]);
          } catch {
            continue;
          }

          if (eventType === "log") {
            const line = (payload.line as string) ?? "";
            updateLastAssistant((last) => ({
              ...last,
              processLogs: [...(last.processLogs || []), line],
            }));
            continue;
          }

          if (eventType === "stream") {
            const event = payload as unknown as StreamEvent;
            if (event.type === "session" || event.type === "done") continue;
            updateLastAssistant((last) => ({
              ...last,
              content: event.type === "content" ? `${last.content}${event.content}` : last.content,
              events: [...(last.events || []), event],
            }));
            continue;
          }

          if (eventType === "result") {
            updateLastAssistant((last) => ({
              ...last,
              result: {
                success: Boolean(payload.success),
                data: ((payload.data as Record<string, unknown>) ?? {}),
                elapsedMs: typeof payload.elapsed_ms === "number" ? payload.elapsed_ms : undefined,
              },
            }));
            continue;
          }

          if (eventType === "error") {
            updateLastAssistant((last) => ({
              ...last,
              error: (payload.detail as string) ?? "Unknown error",
            }));
          }
        }
      }
    } catch (err: unknown) {
      if (controller.signal.aborted) return;
      updateLastAssistant((last) => ({
        ...last,
        error: err instanceof Error ? err.message : String(err),
      }));
    } finally {
      if (!controller.signal.aborted) setStreaming(false);
    }
  };

  return (
    <div className="flex h-full min-h-0 flex-col gap-4">
      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="space-y-5 pb-4">
          {messages.map((msg, i) => (
            <PlaygroundChatTurn
              key={`${msg.role}-${i}`}
              msg={msg}
              isStreaming={streaming}
              isLatestAssistant={i === messages.length - 1}
            />
          ))}
        </div>
      </div>
      <div className="sticky bottom-0 z-10 shrink-0 border-t border-[var(--border)] bg-[var(--background)]/96 pt-2 backdrop-blur">
        <div className="rounded-[22px] border border-[var(--border)]/60 bg-[var(--background)]/84 px-3 py-2.5 shadow-[0_1px_2px_rgba(15,23,42,0.03)]">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            rows={2}
            placeholder={`${t("Try")} ${t(getCapabilityLabel(capability.name))}...`}
            className="w-full resize-none bg-transparent text-[13px] leading-5 text-[var(--foreground)] outline-none placeholder:text-[var(--muted-foreground)]"
          />
          <div className="mt-2 flex items-center justify-between gap-3">
            <div className="text-[11px] text-[var(--muted-foreground)]">
              {t("Enter to send, Shift+Enter for a new line.")}
            </div>
            <button
              onClick={send}
              disabled={!input.trim() || streaming}
              className="inline-flex items-center gap-2 rounded-full bg-[var(--muted)] px-4 py-1.5 text-[12px] font-medium text-[var(--foreground)] transition-colors hover:bg-[var(--muted)]/80 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {streaming ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
              {streaming ? t("Running...") : t("Send")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main Page                                                          */
/* ------------------------------------------------------------------ */

export default function PlaygroundPage() {
  const { t, i18n } = useTranslation();
  const {
    state: unifiedChatState,
    sendMessage,
    cancelStreamingTurn,
    setTools,
    setCapability,
    setKBs,
    setTutorPack,
    setLanguage,
    selectedSessionId,
  } = useUnifiedChat();
  const [tools, setToolsList] = useState<ToolInfo[]>([]);
  const [capabilities, setCapabilities] = useState<CapabilityInfo[]>([]);
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
  const [capabilityConfigs, setCapabilityConfigs] = useState<CapabilityPlaygroundConfigMap>({});
  const [activeKind, setActiveKind] = useState<"tool" | "capability">("tool");
  const [activeName, setActiveName] = useState<string>("");
  const [rightPanelCollapsed, setRightPanelCollapsed] = useState(false);
  const [rightPanelWidth, setRightPanelWidth] = useState<"compact" | "comfortable" | "expanded">(
    "comfortable",
  );
  const [loading, setLoading] = useState(true);
  const [availableTutorPacks, setAvailableTutorPacks] = useState<TutorPackOption[]>([]);
  const [pendingTutorPackKnowledgeBase, setPendingTutorPackKnowledgeBase] = useState("");

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const [pluginRes, knowledgeBaseList] = await Promise.all([
          fetch(apiUrl("/api/v1/plugins/list")),
          listKnowledgeBases(),
        ]);
        const data = await pluginRes.json();
        const visibleTools = (data.tools || []).filter(
          (tool: ToolInfo) => !FRONTEND_HIDDEN_TOOLS.has(tool.name),
        );
        const visibleCapabilities = (data.capabilities || []).map((cap: CapabilityInfo) => ({
          ...cap,
          tools_used: filterFrontendTools(cap.tools_used ?? []),
        }));

        setToolsList(visibleTools);
        setCapabilities(visibleCapabilities);
        setCapabilityConfigs(loadCapabilityPlaygroundConfigs());
        setKnowledgeBases(knowledgeBaseList);
        const tutorPacks = knowledgeBaseList
          .filter((kb) => kb.status === "ready" || kb.status === "offline-cached" || !kb.status)
          .map((kb) => ({
            name: kb.name,
            knowledgeBase: kb.name,
            subject: kb.metadata?.subject ?? null,
            grade: kb.metadata?.grade ?? null,
            owner: kb.metadata?.owner ?? null,
            language: kb.metadata?.language ?? null,
          }));
        setAvailableTutorPacks(tutorPacks);

        const defaultCapability =
          visibleCapabilities.find((cap: CapabilityInfo) => cap.name === "chat") ??
          visibleCapabilities[0];
        if (defaultCapability) {
          setActiveKind("capability");
          setActiveName(defaultCapability.name);
        } else if (visibleTools.length) {
          setActiveKind("tool");
          setActiveName(visibleTools[0].name);
        }
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const capabilityCatalog = capabilities;

  const activeTool = tools.find((t) => t.name === activeName);
  const activeCapability = capabilityCatalog.find((c) => c.name === activeName);
  const selectedTutorPack = unifiedChatState.tutorPack;
  const requiresTutorPackSelection =
    !selectedSessionId &&
    activeCapability?.name === "chat" &&
    availableTutorPacks.length > 1 &&
    !selectedTutorPack;
  const chatDisabledReason =
    selectedTutorPack?.status === "missing"
      ? t("Gói gia sư này không còn khả dụng. Bạn vẫn có thể xem lịch sử nhưng chưa thể gửi thêm tin nhắn.")
      : activeCapability?.name === "chat" && availableTutorPacks.length === 0
        ? t("Chưa có Gói gia sư khả dụng. Hãy import một gói từ Marketplace trước.")
        : requiresTutorPackSelection
          ? t("Chọn Gói gia sư trước khi bắt đầu cuộc trò chuyện này.")
          : null;
  const isChatSendDisabled = Boolean(chatDisabledReason);
  const activeCapabilityConfig = useMemo(
    () =>
      activeCapability
        ? resolveCapabilityPlaygroundConfig(
            capabilityConfigs,
            activeCapability.name,
            activeCapability.tools_used ?? [],
          )
        : null,
    [activeCapability, capabilityConfigs],
  );
  const activeDeepQuestionConfig = useMemo(
    () => normalizeDeepQuestionConfig((activeCapabilityConfig?.config as Record<string, unknown> | undefined)),
    [activeCapabilityConfig?.config],
  );
  const activeDeepResearchConfig = useMemo(
    () =>
      normalizeResearchConfig(
        activeCapabilityConfig?.config as Record<string, unknown> | undefined,
      ),
    [activeCapabilityConfig?.config],
  );
  const activeLabel =
    activeKind === "tool"
      ? activeTool
        ? t(getToolLabel(activeTool.name))
        : t("Tools")
      : activeCapability
        ? t(getCapabilityLabel(activeCapability.name))
        : t("Capabilities");

  const activeDescription =
    activeKind === "tool"
      ? activeTool
        ? getToolDescription(activeTool.description, t)
        : ""
      : activeCapability
        ? getCapabilityDescription(activeCapability.description, t)
        : "";

  const rightPanelHeaderActions = (
    <div className="inline-flex rounded-xl border border-[var(--border)] bg-[var(--background)]/80 p-1">
      <button
        type="button"
        onClick={() => setRightPanelWidth("compact")}
        title={t("Compact panel")}
        aria-label={t("Compact panel")}
        className={`rounded-lg p-1.5 transition ${
          rightPanelWidth === "compact"
            ? "bg-[var(--foreground)] text-[var(--background)]"
            : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
        }`}
      >
        <Columns3 size={14} />
      </button>
      <button
        type="button"
        onClick={() => setRightPanelWidth("comfortable")}
        title={t("Comfortable panel")}
        aria-label={t("Comfortable panel")}
        className={`rounded-lg p-1.5 transition ${
          rightPanelWidth === "comfortable"
            ? "bg-[var(--foreground)] text-[var(--background)]"
            : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
        }`}
      >
        <ChevronsLeftRight size={14} />
      </button>
      <button
        type="button"
        onClick={() => setRightPanelWidth("expanded")}
        title={t("Expanded panel")}
        aria-label={t("Expanded panel")}
        className={`rounded-lg p-1.5 transition ${
          rightPanelWidth === "expanded"
            ? "bg-[var(--foreground)] text-[var(--background)]"
            : "text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
        }`}
      >
        <Expand size={14} />
      </button>
    </div>
  );

  const persistCapabilityConfig = (capabilityName: string, next: CapabilityPlaygroundConfig) => {
    setCapabilityConfigs((prev) =>
      saveCapabilityPlaygroundConfig(prev, capabilityName, next),
    );
  };

  const toggleCapabilityTool = (toolName: string) => {
    if (!activeCapability || !activeCapabilityConfig) return;
    const allowedTools = filterFrontendTools(activeCapability.tools_used ?? []);
    if (!allowedTools.includes(toolName)) return;

    const enabledSet = new Set(activeCapabilityConfig.enabledTools);
    if (enabledSet.has(toolName)) enabledSet.delete(toolName);
    else enabledSet.add(toolName);

    const defaultKb =
      knowledgeBases.find((kb) => kb.is_default)?.name ??
      knowledgeBases[0]?.name ??
      "";

    persistCapabilityConfig(activeCapability.name, {
      enabledTools: allowedTools.filter((name) => enabledSet.has(name)),
      knowledgeBase:
        activeCapabilityConfig.knowledgeBase || (enabledSet.has("rag") ? defaultKb : ""),
      config: activeCapabilityConfig.config,
    });
  };

  const setCapabilityKnowledgeBase = (knowledgeBase: string) => {
    if (!activeCapability || !activeCapabilityConfig) return;
    persistCapabilityConfig(activeCapability.name, {
      enabledTools: activeCapabilityConfig.enabledTools,
      knowledgeBase,
      config: activeCapabilityConfig.config,
    });
  };

  const setDeepQuestionConfig = (next: DeepQuestionFormConfig) => {
    if (!activeCapability || !activeCapabilityConfig) return;
    persistCapabilityConfig(activeCapability.name, {
      enabledTools: activeCapabilityConfig.enabledTools,
      knowledgeBase: activeCapabilityConfig.knowledgeBase,
      config: next as unknown as Record<string, unknown>,
    });
  };

  const setDeepResearchConfig = (next: DeepResearchFormConfig) => {
    if (!activeCapability || !activeCapabilityConfig) return;
    persistCapabilityConfig(activeCapability.name, {
      enabledTools: activeCapabilityConfig.enabledTools,
      knowledgeBase: activeCapabilityConfig.knowledgeBase,
      config: next as unknown as Record<string, unknown>,
    });
  };

  useEffect(() => {
    if (!activeCapability || activeCapability.name !== "chat" || !activeCapabilityConfig) return;
    setCapability("chat");
    setTools(activeCapabilityConfig.enabledTools);
    setKBs(
      selectedTutorPack?.knowledgeBase
        ? [selectedTutorPack.knowledgeBase]
        : activeCapabilityConfig.knowledgeBase
          ? [activeCapabilityConfig.knowledgeBase]
          : [],
    );
  }, [activeCapability, activeCapabilityConfig, selectedTutorPack, setCapability, setKBs, setTools]);

  useEffect(() => {
    setLanguage(i18n.language);
  }, [i18n.language, setLanguage]);

  useEffect(() => {
    if (!selectedSessionId) return;
    setActiveKind("capability");
    setActiveName("chat");
  }, [selectedSessionId]);

  useEffect(() => {
    if (activeCapability?.name !== "chat" || loading) return;
    if (selectedSessionId) return;
    if (selectedTutorPack) return;
    if (availableTutorPacks.length !== 1) return;
    const onlyPack = availableTutorPacks[0];
    setPendingTutorPackKnowledgeBase(onlyPack.knowledgeBase);
    setTutorPack({
      name: onlyPack.name,
      knowledgeBase: onlyPack.knowledgeBase,
      status: "available",
    });
    setKBs([onlyPack.knowledgeBase]);
  }, [
    activeCapability,
    availableTutorPacks,
    loading,
    selectedSessionId,
    selectedTutorPack,
    setKBs,
    setTutorPack,
  ]);

  useEffect(() => {
    if (!selectedTutorPack) return;
    const stillAvailable = availableTutorPacks.some(
      (pack) => pack.knowledgeBase === selectedTutorPack.knowledgeBase,
    );
    if (!stillAvailable && selectedTutorPack.status !== "missing") {
      setTutorPack({ ...selectedTutorPack, status: "missing" });
      return;
    }
    if (stillAvailable && selectedTutorPack.status === "missing") {
      setTutorPack({ ...selectedTutorPack, status: "available" });
    }
  }, [availableTutorPacks, selectedTutorPack, setTutorPack]);

  const handleTutorPackSelection = (knowledgeBase: string) => {
    setPendingTutorPackKnowledgeBase(knowledgeBase);
    const selectedPack = availableTutorPacks.find((pack) => pack.knowledgeBase === knowledgeBase);
    if (!selectedPack) {
      setTutorPack(null);
      setKBs([]);
      return;
    }
    const nextTutorPack: TutorPackBinding = {
      name: selectedPack.name,
      knowledgeBase: selectedPack.knowledgeBase,
      status: "available",
    };
    setTutorPack(nextTutorPack);
    setKBs([selectedPack.knowledgeBase]);
  };

  const centerPanel = (
    <main aria-label={t("Conversation workspace")} className="flex h-full min-h-0 flex-col">
      <div className="border-b border-[var(--border)] px-6 py-1.5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
              {t("Conversation workspace")}
            </p>
            <h2 className="mt-0.5 text-base font-semibold tracking-tight text-[var(--foreground)]">
              {activeLabel}
            </h2>
          </div>
          <button
            type="button"
            onClick={() => setRightPanelCollapsed((prev) => !prev)}
            title={rightPanelCollapsed ? t("Open tools and context") : t("Hide tools and context")}
            aria-label={rightPanelCollapsed ? t("Open tools and context") : t("Hide tools and context")}
            className="rounded-xl border border-[var(--border)] bg-[var(--background)]/70 p-1.5 text-[var(--muted-foreground)] transition hover:text-[var(--foreground)]"
          >
            {rightPanelCollapsed ? <PanelRightOpen size={15} /> : <PanelRightClose size={15} />}
          </button>
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-6 py-3">
        {loading ? (
          <div className="flex h-full items-center justify-center">
            <Loader2 className="h-5 w-5 animate-spin text-[var(--muted-foreground)]" />
          </div>
        ) : activeKind === "tool" && activeTool ? (
          <ToolExecutor tool={activeTool} knowledgeBases={knowledgeBases} />
        ) : activeCapability ? (
          activeCapability.name === "chat" ? (
            <PlaygroundSharedChat
              title={t(getCapabilityLabel(activeCapability.name))}
              messages={unifiedChatState.messages}
              isStreaming={unifiedChatState.isStreaming}
              onSend={(content) => sendMessage(content)}
              onCancel={cancelStreamingTurn}
              disabled={isChatSendDisabled}
              disabledReason={chatDisabledReason}
            />
          ) : activeCapability.name === "deep_question" ? (
            <DeepQuestionTester
              key={activeCapability.name}
              capability={activeCapability}
              enabledTools={activeCapabilityConfig?.enabledTools ?? activeCapability.tools_used ?? []}
              knowledgeBase={activeCapabilityConfig?.knowledgeBase ?? ""}
              config={activeDeepQuestionConfig}
              onConfigChange={setDeepQuestionConfig}
            />
          ) : activeCapability.name === "deep_research" ? (
            <DeepResearchTester
              key={activeCapability.name}
              capability={activeCapability}
              enabledTools={activeCapabilityConfig?.enabledTools ?? activeCapability.tools_used ?? []}
              knowledgeBase={activeCapabilityConfig?.knowledgeBase ?? ""}
              config={activeDeepResearchConfig}
              onConfigChange={setDeepResearchConfig}
            />
          ) : (
            <CapabilityTester
              key={activeCapability.name}
              capability={activeCapability}
              enabledTools={activeCapabilityConfig?.enabledTools ?? activeCapability.tools_used ?? []}
              knowledgeBase={activeCapabilityConfig?.knowledgeBase ?? ""}
            />
          )
        ) : null}
      </div>
    </main>
  );

  const rightPanel = activeKind === "tool" && activeTool ? (
    <PlaygroundRightPanel
      badge={t("Context panel")}
      title={t(getToolLabel(activeTool.name))}
      description={getToolDescription(activeTool.description, t)}
      headerActions={rightPanelHeaderActions}
    >
      <div className="space-y-6">
        <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/75 px-4 py-4">
          <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
            {t("Current mode")}
          </p>
          <div className="mt-2 text-[14px] font-semibold text-[var(--foreground)]">
            {t(getToolLabel(activeTool.name))}
          </div>
          <p className="mt-1 text-[12px] leading-5 text-[var(--muted-foreground)]">
            {getToolDescription(activeTool.description, t)}
          </p>
        </section>
        <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/78 px-4 py-4">
          <h3 className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
            {t("Knowledge source")}
          </h3>
          <div className="mt-3 space-y-2">
            {knowledgeBases.length ? knowledgeBases.map((kb) => (
              <div
                key={kb.name}
                className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/70 px-3 py-3 text-[13px]"
              >
                {kb.name}
                {kb.is_default ? ` (${t("default")})` : ""}
              </div>
            )) : (
              <p className="text-[13px] text-[var(--muted-foreground)]">{t("No KB")}</p>
            )}
          </div>
        </section>
      </div>
    </PlaygroundRightPanel>
  ) : activeCapability ? (
    <PlaygroundRightPanel
      badge={t("Context panel")}
      title={t(getCapabilityLabel(activeCapability.name))}
      description={t("Run a focused conversation here without leaving the playground.")}
      headerActions={rightPanelHeaderActions}
    >
      <div className="space-y-6">
        <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/75 px-4 py-4">
          <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
            {t("Current mode")}
          </p>
          <div className="mt-2 text-[14px] font-semibold text-[var(--foreground)]">
            {t(getCapabilityLabel(activeCapability.name))}
          </div>
          <p className="mt-1 text-[12px] leading-5 text-[var(--muted-foreground)]">
            {getCapabilityDescription(activeCapability.description, t)}
          </p>
        </section>
        {activeCapability.name === "chat" ? (
          <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/78 px-4 py-4">
            <h3 className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
              {t("Gói gia sư")}
            </h3>
            {!selectedSessionId && availableTutorPacks.length > 1 ? (
              <div className="mt-3 space-y-3">
                <select
                  value={pendingTutorPackKnowledgeBase}
                  onChange={(e) => handleTutorPackSelection(e.target.value)}
                  className="w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-3 py-3 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
                >
                  <option value="">{t("Chọn gói gia sư")}</option>
                  {availableTutorPacks.map((pack) => (
                    <option key={pack.knowledgeBase} value={pack.knowledgeBase}>
                      {pack.name}
                    </option>
                  ))}
                </select>
                <p className="text-[12px] leading-5 text-[var(--muted-foreground)]">
                  {t("Mỗi cuộc trò chuyện sẽ khóa vào một Gói gia sư từ lúc bắt đầu và không đổi giữa chừng.")}
                </p>
              </div>
            ) : selectedTutorPack ? (
              <div className="mt-3 rounded-2xl border border-[var(--border)] bg-[var(--background)]/70 px-3 py-3">
                <div className="text-[13px] font-medium text-[var(--foreground)]">
                  {selectedTutorPack.name}
                </div>
                {selectedTutorPack.status === "missing" ? (
                  <p className="mt-2 text-[12px] leading-5 text-amber-700">
                    {t("Gói gia sư này không còn khả dụng. Bạn vẫn có thể xem lịch sử nhưng chưa thể gửi thêm tin nhắn.")}
                  </p>
                ) : (
                  <p className="mt-1 text-[12px] leading-5 text-[var(--muted-foreground)]">
                    {t("Cuộc trò chuyện này đang bám theo gói gia sư đã khóa cho session hiện tại.")}
                  </p>
                )}
              </div>
            ) : (
              <p className="mt-3 text-[13px] text-[var(--muted-foreground)]">
                {availableTutorPacks.length === 1
                  ? t("Gói gia sư sẽ được gán tự động cho cuộc trò chuyện mới.")
                  : t("Chưa có Gói gia sư khả dụng. Hãy import từ Marketplace trước khi bắt đầu chat.")}
              </p>
            )}
          </section>
        ) : null}
        <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/78 px-4 py-4">
          <h3 className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
            {t("Enabled tools")}
          </h3>
          {!!activeCapability.tools_used?.length ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {activeCapability.tools_used.map((tool) => {
                const TIcon = getToolIcon(tool);
                const enabled = activeCapabilityConfig?.enabledTools.includes(tool) ?? true;
                return (
                  <button
                    key={`${activeCapability.name}-${tool}`}
                    type="button"
                    onClick={() => toggleCapabilityTool(tool)}
                    className={`inline-flex items-center gap-2 rounded-full border px-3 py-2 text-[12px] font-medium transition ${
                      enabled
                        ? "border-[var(--foreground)]/10 bg-[var(--background)] text-[var(--foreground)]"
                        : "border-[var(--border)] bg-transparent text-[var(--muted-foreground)]"
                    }`}
                  >
                    <TIcon size={13} strokeWidth={1.7} />
                    {t(getToolLabel(tool))}
                  </button>
                );
              })}
            </div>
          ) : (
            <p className="mt-3 text-[13px] text-[var(--muted-foreground)]">
              {t("This capability runs without optional tools.")}
            </p>
          )}
        </section>

        {activeCapability.name !== "chat" && activeCapabilityConfig?.enabledTools.includes("rag") ? (
          <section className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/78 px-4 py-4">
            <h3 className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
              {t("Knowledge source")}
            </h3>
            <select
              value={activeCapabilityConfig.knowledgeBase}
              onChange={(e) => setCapabilityKnowledgeBase(e.target.value)}
              className="mt-3 w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-3 py-3 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--primary)]/40"
            >
              <option value="">{t("Select knowledge base...")}</option>
              {knowledgeBases.map((kb) => (
                <option key={kb.name} value={kb.name}>
                  {kb.name}
                  {kb.is_default ? ` (${t("default")})` : ""}
                </option>
              ))}
            </select>
          </section>
        ) : null}
      </div>
    </PlaygroundRightPanel>
  ) : null;

  return (
    <PlaygroundWorkspaceShell
      rightCollapsed={rightPanelCollapsed}
      rightWidth={rightPanelWidth}
      center={centerPanel}
      right={rightPanel}
    />
  );
}
