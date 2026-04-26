"use client";

import { type ReactNode, useEffect, useMemo, useState } from "react";
import { Download, Loader2, Plus, Save } from "lucide-react";
import { useTranslation } from "react-i18next";

import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import {
  createAgentSpec,
  exportAgentSpec,
  getAgentSpec,
  listAgentSpecs,
  type AgentSpecDetail,
  type AgentSpecUpsertPayload,
  updateAgentSpec,
} from "@/lib/agent-spec-api";

const MANUAL_FILES = ["CURRICULUM.md", "ASSESSMENT.md", "WORKFLOW.md", "KNOWLEDGE.md", "MARKETPLACE.md"] as const;
type ManualFile = (typeof MANUAL_FILES)[number];

function emptyDraft(): AgentSpecDetail {
  return {
    agent_id: "",
    display_name: "",
    description: "",
    version: 0,
    files: {
      "IDENTITY.md": "# Identity\n",
      "SOUL.md": "# Soul\n",
      "CURRICULUM.md": "# Curriculum\n\n## Core Topics\n\n- Add the priority topics for this agent.\n",
      "RULES.md": "# Rules\n",
      "ASSESSMENT.md": "# Assessment\n\n## Evidence Signals\n\n- Define what the agent should watch for.\n",
      "WORKFLOW.md": "# Workflow\n\n## Session Flow\n\n1. Teach\n2. Practice\n3. Check\n4. Remediate\n",
      "KNOWLEDGE.md": "# Knowledge\n\n## Retrieval Policy\n\n- Prefer teacher-authored materials first.\n",
      "MARKETPLACE.md": "# Marketplace\n\n## Metadata\n\n- Audience:\n- Difficulty:\n- Share status: private\n",
    },
    structured: {
      identity: {
        agent_name: "",
        subject: "",
        grade_band: "",
        tone: "",
        primary_language: "",
        persona_summary: "",
      },
      soul: {
        teaching_philosophy: "",
        when_student_wrong: "",
        when_student_stuck: "",
        encouragement_style: "",
      },
      rules: {
        do_not_solve_directly: "yes",
        max_session_minutes: "",
        hint_policy: "",
        escalation_rule: "",
        guardrails: "",
      },
    },
    summary: {
      subject: "",
      language: "",
      teaching_philosophy: "",
      guardrails: "",
    },
  };
}

function slugify(value: string): string {
  return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export default function SpecPackAuthoringTab({ onToast }: { onToast: (message: string) => void }) {
  const { t } = useTranslation();
  const [packs, setPacks] = useState<AgentSpecDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string>("");
  const [draft, setDraft] = useState<AgentSpecDetail>(emptyDraft());
  const [activeManualFile, setActiveManualFile] = useState<ManualFile>("CURRICULUM.md");
  const [saving, setSaving] = useState(false);
  const [exporting, setExporting] = useState(false);

  async function reloadList(preferredId?: string) {
    const items = await listAgentSpecs();
    const details = await Promise.all(items.map((item) => getAgentSpec(item.agent_id)));
    setPacks(details);
    if (!details.length) {
      setSelectedId("");
      setDraft(emptyDraft());
      return;
    }
    const nextId = preferredId && details.some((item) => item.agent_id === preferredId)
      ? preferredId
      : details[0].agent_id;
    setSelectedId(nextId);
    const selected = details.find((item) => item.agent_id === nextId);
    if (selected) {
      setDraft(selected);
    }
  }

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        await reloadList();
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const runtimeSummary = useMemo(
    () => [
      draft.structured.identity.subject || t("No subject yet"),
      draft.structured.identity.primary_language || t("No language yet"),
      draft.structured.rules.do_not_solve_directly || t("No direct-answer rule yet"),
    ],
    [draft, t],
  );

  const currentPreview = draft.files[activeManualFile] || "";

  function beginNewPack() {
    setSelectedId("");
    setDraft(emptyDraft());
    setActiveManualFile("CURRICULUM.md");
  }

  async function selectPack(agentId: string) {
    setSelectedId(agentId);
    const detail = await getAgentSpec(agentId);
    setDraft(detail);
  }

  async function saveDraft() {
    const resolvedAgentId = draft.version > 0 ? draft.agent_id : slugify(draft.agent_id || draft.display_name);
    if (!resolvedAgentId) {
      onToast(t("Enter a name or agent ID before saving."));
      return;
    }
    const payload: AgentSpecUpsertPayload = {
      agent_id: resolvedAgentId,
      display_name: draft.display_name.trim() || resolvedAgentId,
      description: draft.description,
      structured: draft.structured,
      files: Object.fromEntries(MANUAL_FILES.map((filename) => [filename, draft.files[filename] ?? ""])),
    };

    setSaving(true);
    try {
      const saved = draft.version > 0
        ? await updateAgentSpec(resolvedAgentId, payload)
        : await createAgentSpec(payload);
      setDraft(saved);
      setSelectedId(saved.agent_id);
      await reloadList(saved.agent_id);
      onToast(
        draft.version > 0
          ? t("Spec pack saved.")
          : t("Spec pack created."),
      );
    } catch (error) {
      onToast(error instanceof Error ? error.message : t("Failed to save spec pack."));
    } finally {
      setSaving(false);
    }
  }

  async function exportDraft() {
    if (!draft.agent_id) {
      onToast(t("Save the pack before exporting."));
      return;
    }
    setExporting(true);
    try {
      const blob = await exportAgentSpec(draft.agent_id);
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `${draft.agent_id}-spec-pack.zip`;
      anchor.click();
      URL.revokeObjectURL(url);
      onToast(t("Spec pack exported."));
    } catch (error) {
      onToast(error instanceof Error ? error.message : t("Failed to export spec pack."));
    } finally {
      setExporting(false);
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[280px_minmax(0,1fr)_320px]">
      <aside className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
              {t("Class tutoring setup")}
            </p>
            <h2 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Shape how the tutor teaches this class")}
            </h2>
          </div>
          <button
            onClick={beginNewPack}
            className="inline-flex items-center gap-1 rounded-lg border border-[var(--border)] px-2.5 py-1.5 text-[12px] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
          >
            <Plus className="h-3.5 w-3.5" />
            {t("New")}
          </button>
        </div>
        {loading ? (
          <div className="flex min-h-[120px] items-center justify-center">
            <Loader2 className="h-4 w-4 animate-spin text-[var(--muted-foreground)]" />
          </div>
        ) : packs.length === 0 ? (
          <div className="rounded-xl border border-dashed border-[var(--border)] p-4 text-[13px] text-[var(--muted-foreground)]">
            {t("No spec packs yet. Start with a new teacher-defined agent.")}
          </div>
        ) : (
          <div className="space-y-2">
            {packs.map((pack) => {
              const isActive = selectedId === pack.agent_id;
              return (
                <button
                  key={pack.agent_id}
                  onClick={() => void selectPack(pack.agent_id)}
                  className={`w-full rounded-xl border px-3 py-3 text-left transition-colors ${
                    isActive
                      ? "border-[var(--primary)] bg-[var(--primary)]/6"
                      : "border-[var(--border)] hover:border-[var(--foreground)]/20"
                  }`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <p className="text-[13px] font-medium text-[var(--foreground)]">{pack.display_name}</p>
                    <span className="rounded-full bg-[var(--muted)] px-2 py-0.5 text-[10px] text-[var(--muted-foreground)]">
                      v{pack.version}
                    </span>
                  </div>
                  <p className="mt-1 text-[11px] text-[var(--muted-foreground)]">{pack.agent_id}</p>
                  <p className="mt-2 line-clamp-2 text-[12px] text-[var(--muted-foreground)]">
                    {pack.description || t("No description yet.")}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </aside>

      <section className="space-y-5">
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-5">
          <div className="mb-4 flex items-center justify-between gap-4">
            <div>
              <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                {t("Teacher controls")}
              </p>
              <h2 className="mt-1 text-[18px] font-semibold text-[var(--foreground)]">
                {t("Choose class fit, support style, and guardrails")}
              </h2>
              <p className="mt-2 max-w-[680px] text-[13px] text-[var(--muted-foreground)]">
                {t("IDENTITY sets who this tutor is for, SOUL shapes how it responds when students are wrong or stuck, and RULES keep help within your classroom boundaries.")}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => void exportDraft()}
                disabled={exporting || !draft.agent_id}
                className="inline-flex items-center gap-1.5 rounded-lg border border-[var(--border)] px-3 py-2 text-[12px] text-[var(--muted-foreground)] disabled:opacity-40"
              >
                {exporting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Download className="h-3.5 w-3.5" />}
                {t("Export")}
              </button>
              <button
                onClick={() => void saveDraft()}
                disabled={saving}
                className="inline-flex items-center gap-1.5 rounded-lg bg-[var(--primary)] px-3 py-2 text-[12px] font-medium text-[var(--primary-foreground)] disabled:opacity-40"
              >
                {saving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Save className="h-3.5 w-3.5" />}
                {draft.version > 0 ? t("Save") : t("Create")}
              </button>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <LabeledInput label={t("Display name")} value={draft.display_name} onChange={(value) => setDraft((current) => ({ ...current, display_name: value }))} />
            <LabeledInput
              label={t("Agent ID")}
              value={draft.version > 0 ? draft.agent_id : draft.agent_id}
              disabled={draft.version > 0}
              onChange={(value) => setDraft((current) => ({ ...current, agent_id: slugify(value) }))}
            />
          </div>
          <LabeledTextarea
            label={t("Description")}
            rows={3}
            value={draft.description}
            onChange={(value) => setDraft((current) => ({ ...current, description: value }))}
          />
        </div>

        <StructuredSection
          title={t("IDENTITY.md")}
          description={t("Choose the subject, student level, tone, and language students will experience.")}
        >
          <div className="grid gap-4 md:grid-cols-2">
            <LabeledInput label={t("Agent name")} value={draft.structured.identity.agent_name} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, agent_name: value } } }))} />
            <LabeledInput label={t("Subject")} value={draft.structured.identity.subject} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, subject: value } } }))} />
            <LabeledInput label={t("Grade band")} value={draft.structured.identity.grade_band} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, grade_band: value } } }))} />
            <LabeledInput label={t("Primary language")} value={draft.structured.identity.primary_language} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, primary_language: value } } }))} />
          </div>
          <LabeledInput label={t("Tone")} value={draft.structured.identity.tone} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, tone: value } } }))} />
          <LabeledTextarea label={t("Persona summary")} rows={3} value={draft.structured.identity.persona_summary} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, identity: { ...current.structured.identity, persona_summary: value } } }))} />
        </StructuredSection>

        <StructuredSection
          title={t("SOUL.md")}
          description={t("Decide how the tutor encourages, scaffolds, and responds when a student is wrong or losing confidence.")}
        >
          <LabeledTextarea label={t("Teaching philosophy")} rows={4} value={draft.structured.soul.teaching_philosophy} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, teaching_philosophy: value } } }))} />
          <LabeledTextarea label={t("When the student is wrong")} rows={4} value={draft.structured.soul.when_student_wrong} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, when_student_wrong: value } } }))} />
          <LabeledTextarea label={t("When the student is stuck")} rows={4} value={draft.structured.soul.when_student_stuck} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, when_student_stuck: value } } }))} />
          <LabeledTextarea label={t("Encouragement style")} rows={3} value={draft.structured.soul.encouragement_style} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, encouragement_style: value } } }))} />
        </StructuredSection>

        <StructuredSection
          title={t("RULES.md")}
          description={t("Set clear classroom boundaries such as hint limits, session expectations, and when the tutor should escalate.")}
        >
          <div className="grid gap-4 md:grid-cols-2">
            <LabeledInput label={t("Do not solve directly")} value={draft.structured.rules.do_not_solve_directly} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, rules: { ...current.structured.rules, do_not_solve_directly: value } } }))} />
            <LabeledInput label={t("Max session minutes")} value={draft.structured.rules.max_session_minutes} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, rules: { ...current.structured.rules, max_session_minutes: value } } }))} />
            <LabeledInput label={t("Hint policy")} value={draft.structured.rules.hint_policy} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, rules: { ...current.structured.rules, hint_policy: value } } }))} />
            <LabeledInput label={t("Escalation rule")} value={draft.structured.rules.escalation_rule} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, rules: { ...current.structured.rules, escalation_rule: value } } }))} />
          </div>
          <LabeledTextarea label={t("Guardrails")} rows={4} value={draft.structured.rules.guardrails} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, rules: { ...current.structured.rules, guardrails: value } } }))} />
        </StructuredSection>

        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-5">
          <div className="mb-4">
            <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
              {t("Markdown source of truth")}
            </p>
            <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Manual editing for the remaining files")}
            </h3>
            <p className="mt-2 text-[13px] text-[var(--muted-foreground)]">
              {t("Use these files when you want to define curriculum priorities, assessment signals, remediation flow, knowledge policy, or sharing metadata in your own words.")}
            </p>
          </div>
          <div className="mb-3 flex flex-wrap gap-2">
            {MANUAL_FILES.map((filename) => (
              <button
                key={filename}
                onClick={() => setActiveManualFile(filename)}
                className={`rounded-lg px-3 py-1.5 text-[12px] transition-colors ${
                  activeManualFile === filename
                    ? "bg-[var(--primary)] text-[var(--primary-foreground)]"
                    : "bg-[var(--muted)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
                }`}
              >
                {filename}
              </button>
            ))}
          </div>
          <textarea
            value={draft.files[activeManualFile] ?? ""}
            onChange={(event) =>
              setDraft((current) => ({
                ...current,
                files: {
                  ...current.files,
                  [activeManualFile]: event.target.value,
                },
              }))
            }
            rows={18}
            className="w-full rounded-xl border border-[var(--border)] bg-transparent px-3 py-3 font-mono text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--ring)]"
          />
        </div>
      </section>

      <aside className="space-y-4">
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
          <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
            {t("Teacher-facing summary")}
          </p>
          <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
            {draft.display_name || t("Unsaved spec pack")}
          </h3>
          <div className="mt-4 space-y-3 text-[13px]">
            <SummaryRow label={t("Subject")} value={draft.structured.identity.subject} />
            <SummaryRow label={t("Language")} value={draft.structured.identity.primary_language} />
            <SummaryRow label={t("Tone")} value={draft.structured.identity.tone} />
            <SummaryRow label={t("What students will feel")} value={runtimeSummary.join(" • ")} />
            <SummaryRow label={t("Version")} value={draft.version > 0 ? `v${draft.version}` : t("New")} />
          </div>
        </div>

        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
          <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
            {t("Markdown preview")}
          </p>
          <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">{activeManualFile}</h3>
          <div className="mt-4 max-h-[520px] overflow-y-auto rounded-xl border border-[var(--border)] bg-[var(--background)]/60 p-3">
            <MarkdownRenderer content={currentPreview || "_No content yet._"} variant="prose" />
          </div>
        </div>
      </aside>
    </div>
  );
}

function StructuredSection({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-5">
      <div className="mb-4">
        <h3 className="text-[16px] font-semibold text-[var(--foreground)]">{title}</h3>
        <p className="mt-1 text-[13px] text-[var(--muted-foreground)]">{description}</p>
      </div>
      <div className="space-y-4">{children}</div>
    </div>
  );
}

function LabeledInput({
  label,
  value,
  onChange,
  disabled = false,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-[12px] font-medium text-[var(--muted-foreground)]">{label}</span>
      <input
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-xl border border-[var(--border)] bg-transparent px-3 py-2 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--ring)] disabled:opacity-60"
      />
    </label>
  );
}

function LabeledTextarea({
  label,
  value,
  onChange,
  rows,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  rows: number;
}) {
  return (
    <label className="block">
      <span className="mb-1 block text-[12px] font-medium text-[var(--muted-foreground)]">{label}</span>
      <textarea
        value={value}
        rows={rows}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-xl border border-[var(--border)] bg-transparent px-3 py-2 text-[13px] leading-6 text-[var(--foreground)] outline-none focus:border-[var(--ring)]"
      />
    </label>
  );
}

function SummaryRow({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[11px] uppercase tracking-[0.16em] text-[var(--muted-foreground)]">{label}</p>
      <p className="mt-1 text-[13px] text-[var(--foreground)]">{value || "—"}</p>
    </div>
  );
}
