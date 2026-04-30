"use client";

import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import type { TFunction } from "i18next";
import { ArrowRight, Download, GraduationCap, Loader2, Plus, Save, Search } from "lucide-react";
import { useTranslation } from "react-i18next";

import MarkdownRenderer from "@/components/common/MarkdownRenderer";
import { buildTutorPackFlowViewModel, buildTutorPackOptions } from "@/components/agents/class-tutor-pack-presenters";
import {
  createAgentSpec,
  exportAgentSpec,
  getAgentSpec,
  getAgentSpecRuntimePolicyAudit,
  type RuntimePolicyAuditPayload,
  listAgentSpecs,
  type AgentSpecDetail,
  type AgentSpecUpsertPayload,
  updateAgentSpec,
} from "@/lib/agent-spec-api";
import { listKnowledgeBases, type KnowledgeBaseSummary } from "@/lib/knowledge-api";

const MANUAL_FILES = ["CURRICULUM.md", "ASSESSMENT.md", "WORKFLOW.md", "KNOWLEDGE.md", "MARKETPLACE.md"] as const;
type ManualFile = (typeof MANUAL_FILES)[number];

function decodeHtmlEntities(value: string): string {
  return value
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&amp;", "&")
    .replaceAll("&quot;", "\"")
    .replaceAll("&#39;", "'");
}

function createEmptyDraft(t: TFunction): AgentSpecDetail {
  return {
    agent_id: "",
    display_name: "",
    description: "",
    linked_knowledge_pack: null,
    version: 0,
    files: {
      "IDENTITY.md": t("Spec template IDENTITY.md"),
      "SOUL.md": t("Spec template SOUL.md"),
      "CURRICULUM.md": t("Spec template CURRICULUM.md"),
      "RULES.md": t("Spec template RULES.md"),
      "ASSESSMENT.md": t("Spec template ASSESSMENT.md"),
      "WORKFLOW.md": t("Spec template WORKFLOW.md"),
      "KNOWLEDGE.md": t("Spec template KNOWLEDGE.md"),
      "MARKETPLACE.md": t("Spec template MARKETPLACE.md"),
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
  const buildEmptyDraft = useCallback(() => createEmptyDraft(t), [t]);
  const isDevRuntimeVisible = process.env.NODE_ENV === "development";
  const [packs, setPacks] = useState<AgentSpecDetail[]>([]);
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBaseSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [knowledgeLoading, setKnowledgeLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string>("");
  const [draft, setDraft] = useState<AgentSpecDetail>(() => buildEmptyDraft());
  const [activeManualFile, setActiveManualFile] = useState<ManualFile>("CURRICULUM.md");
  const [packQuery, setPackQuery] = useState("");
  const [saving, setSaving] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [auditCapability, setAuditCapability] = useState<"chat" | "deep_question" | "deep_solve">("chat");
  const [runtimeAudit, setRuntimeAudit] = useState<RuntimePolicyAuditPayload | null>(null);
  const [auditLoading, setAuditLoading] = useState(false);

  const reloadList = useCallback(async (preferredId?: string) => {
    const items = await listAgentSpecs();
    const details = await Promise.all(items.map((item) => getAgentSpec(item.agent_id)));
    setPacks(details);
    if (!details.length) {
      setSelectedId("");
      setDraft(buildEmptyDraft());
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
  }, [buildEmptyDraft]);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      try {
        await reloadList();
      } finally {
        setLoading(false);
      }
    })();
  }, [reloadList]);

  useEffect(() => {
    void (async () => {
      setKnowledgeLoading(true);
      try {
        setKnowledgeBases(await listKnowledgeBases({ force: true }));
      } finally {
        setKnowledgeLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    if (!isDevRuntimeVisible) {
      setRuntimeAudit(null);
      return;
    }
    if (!draft.agent_id) {
      setRuntimeAudit(null);
      return;
    }
    void (async () => {
      setAuditLoading(true);
      try {
        const payload = await getAgentSpecRuntimePolicyAudit(draft.agent_id, auditCapability);
        setRuntimeAudit(payload);
      } catch {
        setRuntimeAudit(null);
      } finally {
        setAuditLoading(false);
      }
    })();
  }, [auditCapability, draft.agent_id, isDevRuntimeVisible]);

  const tutorFlowLabels = useMemo(
    () => ({
      noPackLinked: t("No linked Knowledge Pack yet"),
      packNotFound: t("Linked Knowledge Pack no longer exists"),
      noSubject: t("No subject yet"),
      noDifficulty: t("No difficulty yet"),
      noObjectives: t("No learning goals yet"),
      noLanguage: t("No language yet"),
      noTone: t("No teaching tone yet"),
      noTeachingStyle: t("No teaching style summary yet"),
      noEscalation: t("No teacher handoff rule yet"),
      linkedStatus: t("Linked"),
      unlinkedStatus: t("Not linked"),
      missingStatus: t("Needs relinking"),
      objectiveCount: (count: number) => t("{{count}} learning goals", { count }),
    }),
    [t],
  );

  const linkedPackView = useMemo(
    () => buildTutorPackFlowViewModel(draft, knowledgeBases, tutorFlowLabels),
    [draft, knowledgeBases, tutorFlowLabels],
  );

  const knowledgePackOptions = useMemo(
    () => buildTutorPackOptions(knowledgeBases),
    [knowledgeBases],
  );

  const filteredPackOptions = useMemo(() => {
    const query = packQuery.trim().toLowerCase();
    if (!query) {
      return knowledgePackOptions;
    }
    return knowledgePackOptions.filter((option) => option.label.toLowerCase().includes(query));
  }, [knowledgePackOptions, packQuery]);

  const currentPreview = decodeHtmlEntities(draft.files[activeManualFile] || "");
  const hasLinkedPack = Boolean(draft.linked_knowledge_pack);
  const canPersistDraft = Boolean(hasLinkedPack && (draft.display_name.trim() || draft.agent_id.trim()));

  function beginNewPack() {
    setSelectedId("");
    setDraft(buildEmptyDraft());
    setActiveManualFile("CURRICULUM.md");
    setPackQuery("");
  }

  async function selectPack(agentId: string) {
    setSelectedId(agentId);
    const detail = await getAgentSpec(agentId);
    setDraft(detail);
    setPackQuery("");
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
      linked_knowledge_pack: draft.linked_knowledge_pack,
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
    <div className="grid items-start gap-6 xl:grid-cols-[minmax(240px,280px)_minmax(0,1fr)] 2xl:grid-cols-[minmax(240px,280px)_minmax(0,1fr)_minmax(280px,320px)]">
      <aside className="min-w-0 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
        <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0">
            <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
              {t("Classroom step 2")}
            </p>
            <h2 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
              {t("Pick the class tutor that teaches each Knowledge Pack")}
            </h2>
          </div>
          <button
            onClick={beginNewPack}
            className="inline-flex shrink-0 items-center gap-1 self-start rounded-lg border border-[var(--border)] px-2.5 py-1.5 text-[12px] text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
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
          <div className="rounded-xl border border-dashed border-[var(--border)] px-4 py-8 text-center">
            <GraduationCap className="mx-auto h-8 w-8 text-[var(--muted-foreground)]" />
            <h3 className="mt-3 text-[15px] font-semibold text-[var(--foreground)]">
              {t("No tutors set up yet")}
            </h3>
            <p className="mt-2 text-[13px] text-[var(--muted-foreground)]">
              {t("Create the first class tutor to define how this classroom should be guided.")}
            </p>
            <button
              type="button"
              onClick={beginNewPack}
              className="mt-4 inline-flex items-center gap-2 rounded-lg bg-[var(--primary)] px-3 py-2 text-[13px] font-medium text-[var(--primary-foreground)]"
            >
              <Plus className="h-4 w-4" />
              {t("Create the first tutor")}
            </button>
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
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-[var(--background)] px-2 py-0.5 text-[10px] text-[var(--muted-foreground)]">
                      {pack.linked_knowledge_pack || t("Not linked yet")}
                    </span>
                  </div>
                  <p className="mt-2 line-clamp-2 text-[12px] text-[var(--muted-foreground)]">
                    {pack.description || t("No description yet.")}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </aside>

      <section className="min-w-0 space-y-5">
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-5">
          <div className="mb-4 flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="min-w-0">
              <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                {t("Step 2 of classroom setup")}
              </p>
              <h2 className="mt-1 text-[18px] font-semibold text-[var(--foreground)]">
                {t("Define how this class tutor teaches the selected Knowledge Pack")}
              </h2>
              <p className="mt-2 max-w-[680px] text-[13px] text-[var(--muted-foreground)]">
                {t("Link this class tutor to one Knowledge Pack so the teaching tone, support moves, and boundaries stay grounded in the same classroom context.")}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2 lg:justify-end">
              <button
                onClick={() => void exportDraft()}
                disabled={exporting || !draft.agent_id || !hasLinkedPack}
                className="inline-flex min-w-[104px] items-center justify-center gap-1.5 rounded-lg border border-[var(--border)] px-3 py-2 text-[12px] text-[var(--muted-foreground)] disabled:opacity-40"
                title={!hasLinkedPack ? t("Select a Knowledge Pack before saving the tutor.") : t("Export tutor configuration")}
              >
                {exporting ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Download className="h-3.5 w-3.5" />}
                {t("Export tutor configuration")}
              </button>
              <button
                onClick={() => void saveDraft()}
                disabled={saving || !canPersistDraft}
                className="inline-flex min-w-[104px] items-center justify-center gap-1.5 rounded-lg bg-[var(--primary)] px-3 py-2 text-[12px] font-medium text-[var(--primary-foreground)] disabled:opacity-40"
                title={canPersistDraft ? undefined : t("Select a Knowledge Pack before saving the tutor.")}
              >
                {saving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Save className="h-3.5 w-3.5" />}
                {draft.version > 0 ? t("Save tutor changes") : t("Save and create tutor")}
              </button>
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_minmax(260px,320px)]">
            <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/60 p-4">
              <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                {t("Linked Knowledge Pack")}
              </p>
              <div className="mt-1 flex items-center justify-between gap-3">
                <h3 className="text-[16px] font-semibold text-[var(--foreground)]">
                  {t("Choose or change the linked pack")}
                </h3>
                <span className={`rounded-full px-2.5 py-1 text-[10px] font-medium ${
                  linkedPackView.statusTone === "linked"
                    ? "bg-emerald-500/12 text-emerald-700"
                    : linkedPackView.statusTone === "missing"
                      ? "bg-amber-500/12 text-amber-700"
                      : "bg-[var(--muted)] text-[var(--muted-foreground)]"
                }`}>
                  {linkedPackView.statusLabel}
                </span>
              </div>
              <p className="mt-2 text-[12px] text-[var(--muted-foreground)]">
                {t("A class tutor should follow one pack at a time so students receive one consistent teaching style for that classroom flow.")}
              </p>
              <div className="mt-4 rounded-xl border border-[var(--border)] bg-[var(--card)]/70 p-3">
                <label className="mb-2 block text-[12px] font-medium text-[var(--muted-foreground)]">
                  {t("Knowledge Pack")}
                </label>
                <div className="relative">
                  <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted-foreground)]" />
                  <input
                    value={packQuery}
                    onChange={(event) => setPackQuery(event.target.value)}
                    placeholder={t("Search or choose a Knowledge Pack…")}
                    className="w-full rounded-lg border border-[var(--border)] bg-transparent py-2 pl-9 pr-3 text-[13px] text-[var(--foreground)] outline-none focus:border-[var(--ring)]"
                  />
                </div>
                <div className="mt-2 max-h-56 overflow-y-auto rounded-lg border border-[var(--border)] bg-[var(--background)]/80 p-1">
                  {knowledgeLoading ? (
                    <div className="px-3 py-2 text-[12px] text-[var(--muted-foreground)]">
                      {t("Loading Knowledge Packs…")}
                    </div>
                  ) : filteredPackOptions.length === 0 ? (
                    <div className="px-3 py-2 text-[12px] text-[var(--muted-foreground)]">
                      {t("No matching Knowledge Packs")}
                    </div>
                  ) : (
                    filteredPackOptions.map((option) => (
                      <button
                        key={option.value}
                        type="button"
                        onClick={() =>
                          setDraft((current) => ({
                            ...current,
                            linked_knowledge_pack: option.value,
                          }))
                        }
                        className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-[13px] transition-colors ${
                          draft.linked_knowledge_pack === option.value
                            ? "bg-[var(--primary)]/8 text-[var(--foreground)]"
                            : "hover:bg-[var(--muted)]"
                        }`}
                      >
                        <span>{option.label}</span>
                        {draft.linked_knowledge_pack === option.value ? (
                          <span className="text-[11px] font-medium text-[var(--primary)]">{t("Selected")}</span>
                        ) : null}
                      </button>
                    ))
                  )}
                </div>
                {draft.linked_knowledge_pack ? (
                  <button
                    type="button"
                    onClick={() =>
                      setDraft((current) => ({
                        ...current,
                        linked_knowledge_pack: null,
                      }))
                    }
                    className="mt-2 text-[12px] text-[var(--muted-foreground)] underline-offset-2 hover:underline"
                  >
                    {t("Clear selected Knowledge Pack")}
                  </button>
                ) : null}
              </div>
            </div>

            <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)]/60 p-4">
              <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                {t("Classroom flow")}
              </p>
              <h3 className="mt-1 text-[15px] font-semibold text-[var(--foreground)]">
                {t("How this tutor setup fits the pack")}
              </h3>
              <div className="mt-4 rounded-xl border border-dashed border-[var(--border)] p-3 text-[12px] text-[var(--muted-foreground)]">
                <div className="flex items-center gap-2 text-[var(--foreground)]">
                  <ArrowRight className="h-3.5 w-3.5" />
                  {t("Suggested flow")}
                </div>
                <p className="mt-2">
                  {t("1. Finalize the Knowledge Pack. 2. Define how the class tutor teaches it. 3. Let students practice with one coherent classroom setup.")}
                </p>
                <div className="mt-3 space-y-2">
                  <SummaryTile label={t("Current pack")} value={linkedPackView.packName} />
                  <SummaryTile label={t("Status")} value={linkedPackView.statusLabel} />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 grid gap-4 md:grid-cols-2">
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
          title={t("Tutor identity section")}
          description={t("Set who this tutor is for and how students should experience the linked pack in class.")}
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
          title={t("Tutor teaching style section")}
          description={t("Define how this tutor explains the linked pack, encourages students, and responds when they are wrong or stuck.")}
        >
          <LabeledTextarea label={t("Teaching philosophy")} rows={4} value={draft.structured.soul.teaching_philosophy} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, teaching_philosophy: value } } }))} />
          <LabeledTextarea label={t("When the student is wrong")} rows={4} value={draft.structured.soul.when_student_wrong} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, when_student_wrong: value } } }))} />
          <LabeledTextarea label={t("When the student is stuck")} rows={4} value={draft.structured.soul.when_student_stuck} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, when_student_stuck: value } } }))} />
          <LabeledTextarea label={t("Encouragement style")} rows={3} value={draft.structured.soul.encouragement_style} onChange={(value) => setDraft((current) => ({ ...current, structured: { ...current.structured, soul: { ...current.structured.soul, encouragement_style: value } } }))} />
        </StructuredSection>

        <StructuredSection
          title={t("Tutor rules section")}
          description={t("Set the classroom boundaries for this linked tutor, including hint limits and when the case should return to teacher review.")}
        >
          <div className="grid gap-4 md:grid-cols-2">
            <BooleanField
              label={t("Do not solve directly")}
              checked={draft.structured.rules.do_not_solve_directly === "yes"}
              onChange={(checked) =>
                setDraft((current) => ({
                  ...current,
                  structured: {
                    ...current.structured,
                    rules: {
                      ...current.structured.rules,
                      do_not_solve_directly: checked ? "yes" : "no",
                    },
                  },
                }))
              }
            />
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
              {t("Extra classroom details in markdown")}
            </h3>
            <p className="mt-2 text-[13px] text-[var(--muted-foreground)]">
              {t("Use these files only when you need extra detail for curriculum priorities, assessment signals, remediation flow, knowledge policy, or sharing metadata.")}
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
                {t(filename)}
              </button>
            ))}
          </div>
          <textarea
            value={decodeHtmlEntities(draft.files[activeManualFile] ?? "")}
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

      <aside className="min-w-0 space-y-4">
        <div className="min-w-0 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
          <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
            {t("Teacher-facing summary")}
          </p>
          <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
            {draft.display_name || t("Unsaved spec pack")}
          </h3>
          <div className="mt-4 space-y-3 text-[13px]">
            <SummaryRow label={t("Linked Knowledge Pack")} value={linkedPackView.packName} />
            <SummaryRow label={t("Subject")} value={linkedPackView.subject} />
            <SummaryRow label={t("Learning goals")} value={linkedPackView.objectiveSummary} />
            <SummaryRow label={t("Language")} value={linkedPackView.language} />
            <SummaryRow label={t("Tone")} value={linkedPackView.tone} />
            <SummaryRow label={t("What the tutor will emphasize")} value={linkedPackView.teachingPromise} />
            <SummaryRow label={t("When to send back to teacher")} value={linkedPackView.escalationSummary} />
            <SummaryRow label={t("Version")} value={draft.version > 0 ? `v${draft.version}` : t("New")} />
          </div>
        </div>

        {isDevRuntimeVisible ? (
          <div className="min-w-0 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div className="min-w-0">
                <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                  {t("Runtime policy audit")}
                </p>
                <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">
                  {t("Technical runtime check")}
                </h3>
              </div>
              <select
                value={auditCapability}
                onChange={(event) => setAuditCapability(event.target.value as "chat" | "deep_question" | "deep_solve")}
                className="w-full rounded-lg border border-[var(--border)] bg-transparent px-2 py-1 text-[12px] text-[var(--foreground)] sm:w-auto"
              >
                <option value="chat">{t("chat")}</option>
                <option value="deep_question">{t("deep_question")}</option>
                <option value="deep_solve">{t("deep_solve")}</option>
              </select>
            </div>
            {!draft.agent_id ? (
              <p className="mt-3 text-[12px] text-[var(--muted-foreground)]">
                {t("Save the spec pack first to inspect the compiled runtime policy.")}
              </p>
            ) : auditLoading ? (
              <div className="mt-4 flex items-center gap-2 text-[12px] text-[var(--muted-foreground)]">
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                {t("Loading runtime policy audit…")}
              </div>
            ) : runtimeAudit ? (
              <div className="mt-4 space-y-3 text-[12px]">
                <SummaryRow label={t("Capability")} value={runtimeAudit.capability} />
                <SummaryRow
                  label={t("Spec version")}
                  value={runtimeAudit.agent_spec_version != null ? `v${runtimeAudit.agent_spec_version}` : t("Latest")}
                />
                <SummaryRow label={t("Knowledge policy")} value={runtimeAudit.runtime_policy.knowledge_policy} />
                <SummaryRow
                  label={t("Source priority")}
                  value={runtimeAudit.runtime_policy.source_priority.join(" > ")}
                />
                <SummaryRow
                  label={t("Applied slices")}
                  value={runtimeAudit.runtime_policy.debug.applied_slices.join(", ") || t("None")}
                />
                <SummaryRow
                  label={t("Missing slices")}
                  value={runtimeAudit.runtime_policy.debug.missing_slices.join(", ") || t("None")}
                />
                <div className="rounded-xl border border-[var(--border)] bg-[var(--background)]/50 p-3">
                  <p className="text-[11px] uppercase tracking-[0.16em] text-[var(--muted-foreground)]">
                    {t("Slice sources")}
                  </p>
                  <div className="mt-2 space-y-2">
                    {Object.entries(runtimeAudit.runtime_policy.debug.slice_sources).map(([slice, source]) => (
                      <div key={slice} className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between sm:gap-3">
                        <span className="font-medium text-[var(--foreground)] break-words">{slice}</span>
                        <span className="text-left break-words text-[var(--muted-foreground)] sm:text-right">{source}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="mt-3 text-[12px] text-[var(--muted-foreground)]">
                {t("No runtime audit is available for this spec yet.")}
              </p>
            )}
          </div>
        ) : null}

        <div className="min-w-0 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-4">
          <p className="text-[12px] uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
            {t("Markdown preview")}
          </p>
          <h3 className="mt-1 text-[16px] font-semibold text-[var(--foreground)]">{t(activeManualFile)}</h3>
          <div className="mt-4 max-h-[520px] overflow-y-auto rounded-xl border border-[var(--border)] bg-[var(--background)]/60 p-3">
            <MarkdownRenderer content={currentPreview || `_${t("No content yet.")}_`} variant="prose" />
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
    <div className="min-w-0 rounded-2xl border border-[var(--border)] bg-[var(--card)]/40 p-5">
      <div className="mb-4 min-w-0">
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

function BooleanField({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}) {
  const { t } = useTranslation();

  return (
    <label className="flex min-w-0 flex-col gap-3 rounded-xl border border-[var(--border)] bg-transparent px-3 py-2.5 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0 pr-0 sm:pr-3">
        <p className="break-words text-[12px] font-medium text-[var(--foreground)]">{label}</p>
        <p className="mt-1 text-[11px] text-[var(--muted-foreground)]">
          {checked ? t("On") : t("Off")}
        </p>
      </div>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={() => onChange(!checked)}
        className={`relative h-6 w-11 shrink-0 self-start rounded-full transition-colors sm:self-center ${
          checked ? "bg-[var(--primary)]" : "bg-[var(--muted)]"
        }`}
      >
        <span
          className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${
            checked ? "translate-x-5" : "translate-x-0.5"
          }`}
        />
      </button>
    </label>
  );
}

function SummaryRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0">
      <p className="text-[11px] uppercase tracking-[0.16em] text-[var(--muted-foreground)]">{label}</p>
      <p className="mt-1 break-words text-[13px] text-[var(--foreground)]">{value || "—"}</p>
    </div>
  );
}

function SummaryTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)]/60 p-3">
      <p className="text-[11px] uppercase tracking-[0.16em] text-[var(--muted-foreground)]">{label}</p>
      <p className="mt-1 text-[13px] font-medium text-[var(--foreground)]">{value || "—"}</p>
    </div>
  );
}
