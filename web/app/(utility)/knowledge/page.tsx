"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  FileText,
  Loader2,
  PencilLine,
  Plus,
  Sparkles,
  Trash2,
  Upload,
} from "lucide-react";
import { apiUrl, wsUrl } from "@/lib/api";
import {
  invalidateKnowledgeCaches,
  listKnowledgeBases,
  type TeacherPackMetadata,
  updateKnowledgeBaseConfig,
} from "@/lib/knowledge-api";
import { CoreLoopVisibilityStrip } from "@/components/contest/CoreLoopVisibilityStrip";

const ProcessLogs = dynamic(() => import("@/components/common/ProcessLogs"), {
  ssr: false,
});

type WizardStep = "info" | "files" | "done";
type DifficultyValue = "beginner" | "intermediate" | "advanced";

interface FileStatusInfo {
  name: string;
  status: string;
  error?: string;
  updated_at?: string;
}

interface ProgressInfo {
  task_id?: string;
  stage?: string;
  message?: string;
  current?: number;
  total?: number;
  percent?: number;
  progress_percent?: number;
  file_name?: string;
  file_statuses?: FileStatusInfo[];
  error?: string;
}

interface KnowledgeBase {
  name: string;
  is_default?: boolean;
  status?: string;
  progress?: ProgressInfo;
  metadata?: TeacherPackMetadata | null;
  statistics?: {
    raw_documents?: number;
    rag_provider?: string;
    needs_reindex?: boolean;
    status?: string;
    progress?: ProgressInfo;
  };
}

interface ProcessState {
  taskId: string | null;
  label: string;
  logs: string[];
  executing: boolean;
  error: string | null;
}

const EMPTY_PROCESS_STATE: ProcessState = {
  taskId: null,
  label: "",
  logs: [],
  executing: false,
  error: null,
};

const WIZARD_STEPS: Array<{ key: WizardStep; label: string }> = [
  { key: "info", label: "Thông tin" },
  { key: "files", label: "Tài liệu" },
  { key: "done", label: "Hoàn tất" },
];

const DIFFICULTY_OPTIONS: Array<{ value: DifficultyValue; label: string; hint: string }> = [
  { value: "beginner", label: "Cơ bản", hint: "Nội dung nền tảng, dễ bắt đầu." },
  { value: "intermediate", label: "Trung bình", hint: "Cân bằng giữa luyện tập và suy luận." },
  { value: "advanced", label: "Nâng cao", hint: "Phù hợp bài học nhiều thử thách hơn." },
];

const resolveKbStatus = (kb: KnowledgeBase): string => kb.status ?? kb.statistics?.status ?? "unknown";

const resolveProgress = (kb: KnowledgeBase, progressMap: Record<string, ProgressInfo>): ProgressInfo | null =>
  progressMap[kb.name] ?? kb.progress ?? kb.statistics?.progress ?? null;

const difficultyLabel = (value?: string | null): string => {
  switch (value) {
    case "beginner":
      return "Cơ bản";
    case "intermediate":
      return "Trung bình";
    case "advanced":
      return "Nâng cao";
    default:
      return value?.trim() || "Chưa chọn";
  }
};

const statusLabel = (status?: string | null): string => {
  switch (status) {
    case "initializing":
      return "Đang khởi tạo";
    case "processing":
    case "processing_documents":
    case "processing_file":
      return "Đang xử lý";
    case "extracting_items":
      return "Đang hoàn thiện";
    case "completed":
    case "ready":
      return "Hoàn tất";
    case "error":
      return "Có lỗi";
    case "uploaded":
      return "Đã tải lên";
    case "indexed":
      return "Đã lập chỉ mục";
    case "skipped":
      return "Đã bỏ qua";
    case "needs_reindex":
      return "Cần lập chỉ mục lại";
    default:
      return "Chưa rõ";
  }
};

const progressPercent = (progress?: ProgressInfo | null): number => {
  if (!progress) return 0;
  if (typeof progress.progress_percent === "number") return progress.progress_percent;
  if (typeof progress.percent === "number") return progress.percent;
  if (progress.total && progress.current) {
    return Math.round((progress.current / progress.total) * 100);
  }
  return 0;
};

const progressSummaryLabel = (progress?: ProgressInfo | null): string => {
  if (!progress) return "Sẵn sàng tiếp nhận tài liệu";
  if (progress.error) return "Tiến trình gặp lỗi";
  switch (progress.stage) {
    case "initializing":
      return "Đang khởi tạo gói kiến thức";
    case "processing_documents":
      return "Đang xử lý tài liệu";
    case "processing_file":
      return progress.file_name ? `Đang xử lý ${progress.file_name}` : "Đang xử lý từng tài liệu";
    case "extracting_items":
      return "Đang hoàn thiện dữ liệu lập chỉ mục";
    case "completed":
      return "Gói kiến thức đã sẵn sàng";
    case "error":
      return "Không thể hoàn tất lập chỉ mục";
    default:
      return progress.message || "Đang cập nhật trạng thái";
  }
};

const parseLearningObjectives = (value: string): string[] =>
  value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);

const buildTeacherPackMetadata = (input: {
  subject: string;
  difficulty: DifficultyValue;
  curriculum: string;
  learningObjectives: string;
}): TeacherPackMetadata => ({
  subject: input.subject.trim(),
  curriculum: input.curriculum.trim(),
  difficulty: input.difficulty,
  learning_objectives: parseLearningObjectives(input.learningObjectives),
  grade: null,
});

const formatBytes = (bytes: number): string => {
  if (bytes >= 1024 * 1024) {
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }
  if (bytes >= 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }
  return `${bytes} B`;
};

const makeInitialFileStatuses = (files: File[]): FileStatusInfo[] =>
  files.map((file) => ({
    name: file.name,
    status: "uploaded",
  }));

export default function KnowledgePage() {
  const [knowledgeBases, setKnowledgeBases] = useState<KnowledgeBase[]>([]);
  const [progressMap, setProgressMap] = useState<Record<string, ProgressInfo>>({});
  const [loading, setLoading] = useState(true);
  const [pageError, setPageError] = useState<string | null>(null);
  const [wizardStep, setWizardStep] = useState<WizardStep>("info");
  const [creating, setCreating] = useState(false);
  const [createProcess, setCreateProcess] = useState<ProcessState>(EMPTY_PROCESS_STATE);
  const [packName, setPackName] = useState("");
  const [subject, setSubject] = useState("");
  const [difficulty, setDifficulty] = useState<DifficultyValue>("beginner");
  const [curriculum, setCurriculum] = useState("");
  const [learningObjectives, setLearningObjectives] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [activePackName, setActivePackName] = useState<string | null>(null);
  const [detailPackName, setDetailPackName] = useState<string | null>(null);
  const [draftSummary, setDraftSummary] = useState<{
    name: string;
    subject: string;
    difficulty: DifficultyValue;
    curriculum: string;
    learningObjectives: string[];
    fileNames: string[];
  } | null>(null);
  const [editingKbName, setEditingKbName] = useState<string | null>(null);
  const [editSubject, setEditSubject] = useState("");
  const [editDifficulty, setEditDifficulty] = useState<DifficultyValue>("beginner");
  const [editCurriculum, setEditCurriculum] = useState("");
  const [editLearningObjectives, setEditLearningObjectives] = useState("");
  const [savingMetadata, setSavingMetadata] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const socketsRef = useRef<Record<string, WebSocket>>({});
  const logSourceRef = useRef<EventSource | null>(null);

  const closeLogStream = () => {
    logSourceRef.current?.close();
    logSourceRef.current = null;
  };

  const closeProgressSocket = (kbName: string) => {
    socketsRef.current[kbName]?.close();
    delete socketsRef.current[kbName];
  };

  const closeAllProgressSockets = () => {
    Object.values(socketsRef.current).forEach((socket) => socket.close());
    socketsRef.current = {};
  };

  const loadAll = async () => {
    setLoading(true);
    setPageError(null);
    try {
      const nextKbs = await listKnowledgeBases({ force: true });
      setKnowledgeBases(nextKbs);

      for (const kb of nextKbs) {
        const status = resolveKbStatus(kb);
        const progress = kb.progress ?? kb.statistics?.progress;
        const stage = progress?.stage;
        if (
          status &&
          status !== "ready" &&
          status !== "error" &&
          stage !== "completed" &&
          stage !== "error"
        ) {
          setProgressMap((prev) => ({ ...prev, [kb.name]: progress || prev[kb.name] || {} }));
          subscribeProgress(kb.name, progress?.task_id);
        }
      }
    } catch (error) {
      setPageError(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadAll();
    return () => {
      closeAllProgressSockets();
      closeLogStream();
    };
  }, []);

  const subscribeProgress = (kbName: string, expectedTaskId?: string) => {
    closeProgressSocket(kbName);

    const query = expectedTaskId ? `?task_id=${encodeURIComponent(expectedTaskId)}` : "";
    const socket = new WebSocket(wsUrl(`/api/v1/knowledge/${kbName}/progress/ws${query}`));
    socketsRef.current[kbName] = socket;

    socket.onmessage = (event) => {
      try {
        const rawData = JSON.parse(event.data) as {
          type?: string;
          data?: ProgressInfo;
        };
        const progress =
          rawData?.type === "progress" && rawData.data ? rawData.data : (rawData as ProgressInfo);
        if (!progress || typeof progress !== "object") return;
        if (expectedTaskId && progress.task_id && progress.task_id !== expectedTaskId) return;

        setProgressMap((prev) => ({ ...prev, [kbName]: progress }));
        if (progress.stage === "completed" || progress.stage === "error") {
          closeProgressSocket(kbName);
          void loadAll();
        }
      } catch {
        // Ignore malformed progress payloads.
      }
    };

    socket.onerror = () => {
      closeProgressSocket(kbName);
    };

    socket.onclose = () => {
      delete socketsRef.current[kbName];
    };
  };

  const openTaskLogStream = (taskId: string, label: string) => {
    closeLogStream();
    setCreateProcess({
      taskId,
      label,
      logs: [],
      executing: true,
      error: null,
    });

    const source = new EventSource(apiUrl(`/api/v1/knowledge/tasks/${taskId}/stream`));
    logSourceRef.current = source;

    let settled = false;

    source.addEventListener("log", (event) => {
      try {
        const payload = JSON.parse((event as MessageEvent).data) as { line?: string };
        if (!payload.line) return;
        setCreateProcess((prev) => ({ ...prev, logs: [...prev.logs, payload.line!] }));
      } catch {
        // Ignore malformed log events.
      }
    });

    source.addEventListener("complete", () => {
      settled = true;
      setCreateProcess((prev) => ({ ...prev, executing: false }));
      closeLogStream();
    });

    source.addEventListener("failed", (event) => {
      settled = true;
      let detail = "Tiến trình xử lý thất bại.";
      try {
        const payload = JSON.parse((event as MessageEvent).data) as { detail?: string };
        detail = payload.detail || detail;
      } catch {
        // Ignore malformed failure events.
      }
      setCreateProcess((prev) => ({
        ...prev,
        executing: false,
        error: detail,
      }));
      closeLogStream();
    });

    source.onerror = () => {
      if (settled) return;
      setCreateProcess((prev) =>
        prev.executing
          ? { ...prev, executing: false, error: prev.error || "Mất kết nối nhật ký xử lý." }
          : prev,
      );
      closeLogStream();
    };
  };

  const clearWizardInputs = () => {
    setPackName("");
    setSubject("");
    setDifficulty("beginner");
    setCurriculum("");
    setLearningObjectives("");
    setSelectedFiles([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const resetWizard = () => {
    setWizardStep("info");
    setDraftSummary(null);
    setCreateProcess(EMPTY_PROCESS_STATE);
    setActivePackName(null);
    clearWizardInputs();
  };

  const createKnowledgeBase = async () => {
    if (!packName.trim() || !subject.trim() || !curriculum.trim() || !learningObjectives.trim() || !selectedFiles.length) {
      return;
    }

    const kbName = packName.trim();
    const metadata = buildTeacherPackMetadata({
      subject,
      difficulty,
      curriculum,
      learningObjectives,
    });

    setCreating(true);
    setWizardStep("done");
    setActivePackName(kbName);
    setDetailPackName(kbName);
    setDraftSummary({
      name: kbName,
      subject: metadata.subject || "",
      difficulty,
      curriculum: metadata.curriculum || "",
      learningObjectives: metadata.learning_objectives || [],
      fileNames: selectedFiles.map((file) => file.name),
    });

    try {
      const form = new FormData();
      form.append("name", kbName);
      selectedFiles.forEach((file) => form.append("files", file));

      const res = await fetch(apiUrl("/api/v1/knowledge/create"), {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        const error = await res.json().catch(() => ({}));
        throw new Error(error?.detail || "Không thể tạo gói kiến thức.");
      }

      const data = (await res.json()) as { task_id?: string };
      await updateKnowledgeBaseConfig(kbName, metadata);
      invalidateKnowledgeCaches();

      if (data.task_id) {
        setProgressMap((prev) => ({
          ...prev,
          [kbName]: {
            task_id: data.task_id,
            stage: "processing_documents",
            message: "Đang chuẩn bị tài liệu để lập chỉ mục...",
            current: 0,
            total: selectedFiles.length,
            progress_percent: 0,
            file_statuses: makeInitialFileStatuses(selectedFiles),
          },
        }));
        openTaskLogStream(data.task_id, `Đang xử lý ${kbName}`);
        subscribeProgress(kbName, data.task_id);
      }

      clearWizardInputs();
      await loadAll();
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setCreateProcess((prev) => ({
        ...prev,
        executing: false,
        error: message,
        label: prev.label || `Tạo ${kbName}`,
      }));
      setProgressMap((prev) => ({
        ...prev,
        [kbName]: {
          stage: "error",
          message,
          total: selectedFiles.length,
          current: 0,
          file_statuses: selectedFiles.map((file) => ({
            name: file.name,
            status: "error",
            error: message,
          })),
        },
      }));
    } finally {
      setCreating(false);
    }
  };

  const removeSelectedFile = (fileName: string) => {
    setSelectedFiles((prev) => prev.filter((file) => file.name !== fileName));
  };

  const combinedKbs = useMemo(
    () =>
      knowledgeBases.map((kb) => ({
        ...kb,
        status: kb.status ?? kb.statistics?.status,
        progress: resolveProgress(kb, progressMap) || undefined,
      })),
    [knowledgeBases, progressMap],
  );

  const selectedPack =
    combinedKbs.find((kb) => kb.name === (activePackName || detailPackName)) ??
    combinedKbs.find((kb) => kb.name === detailPackName) ??
    null;

  const summaryFileStatuses =
    selectedPack?.progress?.file_statuses?.length
      ? selectedPack.progress.file_statuses
      : draftSummary?.fileNames.map((name) => ({ name, status: "uploaded" })) ?? [];

  const indexedCount = summaryFileStatuses.filter((item) => item.status === "indexed").length;
  const processingCount = summaryFileStatuses.filter((item) =>
    ["uploaded", "processing"].includes(item.status),
  ).length;
  const errorCount = summaryFileStatuses.filter((item) => item.status === "error").length;

  const activeSummary = selectedPack
    ? {
        name: selectedPack.name,
        subject: selectedPack.metadata?.subject ?? draftSummary?.subject ?? "Chưa chọn",
        difficulty:
          selectedPack.metadata?.difficulty ??
          selectedPack.metadata?.grade ??
          draftSummary?.difficulty ??
          null,
        curriculum: selectedPack.metadata?.curriculum ?? draftSummary?.curriculum ?? "Chưa chọn",
        documentCount:
          selectedPack.statistics?.raw_documents ??
          summaryFileStatuses.length ??
          draftSummary?.fileNames.length ??
          0,
        status: selectedPack.progress?.stage ?? selectedPack.status ?? "unknown",
        progress: selectedPack.progress ?? null,
      }
    : draftSummary
      ? {
          name: draftSummary.name,
          subject: draftSummary.subject,
          difficulty: draftSummary.difficulty,
          curriculum: draftSummary.curriculum,
          documentCount: draftSummary.fileNames.length,
          status: "draft",
          progress: null,
        }
      : null;

  const startEditKnowledgePack = (kb: KnowledgeBase) => {
    setEditingKbName(kb.name);
    setDetailPackName(kb.name);
    setEditError(null);
    setEditSubject(kb.metadata?.subject ?? "");
    setEditDifficulty((kb.metadata?.difficulty as DifficultyValue) ?? "beginner");
    setEditCurriculum(kb.metadata?.curriculum ?? "");
    setEditLearningObjectives((kb.metadata?.learning_objectives ?? []).join("\n"));
  };

  const saveKnowledgePackMetadata = async () => {
    if (!editingKbName) return;

    setSavingMetadata(true);
    setEditError(null);
    try {
      await updateKnowledgeBaseConfig(editingKbName, {
        subject: editSubject.trim(),
        curriculum: editCurriculum.trim(),
        difficulty: editDifficulty,
        grade: null,
        learning_objectives: parseLearningObjectives(editLearningObjectives),
      });
      invalidateKnowledgeCaches();
      await loadAll();
      setEditingKbName(null);
    } catch (error) {
      setEditError(error instanceof Error ? error.message : String(error));
    } finally {
      setSavingMetadata(false);
    }
  };

  const deleteKnowledgeBase = async (kbName: string) => {
    if (!window.confirm(`Bạn muốn xóa gói kiến thức "${kbName}"?`)) return;
    await fetch(apiUrl(`/api/v1/knowledge/${kbName}`), { method: "DELETE" });
    invalidateKnowledgeCaches();
    if (detailPackName === kbName) setDetailPackName(null);
    if (activePackName === kbName) setActivePackName(null);
    await loadAll();
  };

  const canContinueInfoStep =
    packName.trim() && subject.trim() && curriculum.trim() && learningObjectives.trim();

  const canSubmitWizard = canContinueInfoStep && selectedFiles.length > 0 && !creating;

  return (
    <div className="h-full overflow-y-auto bg-[var(--background)] [scrollbar-gutter:stable]">
      <div className="mx-auto max-w-6xl px-4 py-8 pb-12 sm:px-6">
        <div className="mb-6 flex flex-col gap-3">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-[var(--foreground)]">
              Gói kiến thức
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-[var(--muted-foreground)]">
              Tạo kho tài liệu lớp học theo một luồng rõ ràng: khai báo thông tin, tải tài liệu,
              theo dõi tiến trình lập chỉ mục, rồi đưa vào sử dụng.
            </p>
          </div>
        </div>

        <CoreLoopVisibilityStrip
          currentStep="Knowledge Pack"
          nextStep="Assessment"
          helperText="Gói kiến thức là lớp nền để phần luyện tập, gia sư và đánh giá dùng chung một nguồn tư liệu đáng tin cậy."
        />

        {pageError && (
          <div className="mb-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            Không thể tải màn hình gói kiến thức: {pageError}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-5 w-5 animate-spin text-[var(--muted-foreground)]" />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
              <section className="overflow-hidden rounded-[28px] border border-[var(--border)] bg-[var(--card)] shadow-sm">
                <div className="border-b border-[var(--border)] bg-[linear-gradient(135deg,rgba(248,244,238,0.95),rgba(255,255,255,0.92))] px-6 py-5">
                  <div className="flex items-center gap-2 text-sm font-medium text-[var(--foreground)]">
                    <Sparkles className="h-4 w-4 text-amber-500" />
                    Luồng tạo gói kiến thức
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {WIZARD_STEPS.map((step, index) => {
                      const isActive = wizardStep === step.key;
                      const isDone =
                        WIZARD_STEPS.findIndex((item) => item.key === wizardStep) > index;
                      return (
                        <button
                          key={step.key}
                          type="button"
                          disabled={step.key === "done" && wizardStep !== "done"}
                          onClick={() => {
                            if (step.key === "info") setWizardStep("info");
                            if (step.key === "files" && canContinueInfoStep) setWizardStep("files");
                          }}
                          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm transition ${
                            isActive
                              ? "border-[var(--foreground)] bg-[var(--foreground)] text-[var(--background)]"
                              : isDone
                                ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                                : "border-[var(--border)] bg-[var(--background)] text-[var(--muted-foreground)]"
                          }`}
                        >
                          <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-black/5 text-[11px]">
                            {index + 1}
                          </span>
                          {step.label}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div className="px-6 py-6">
                  {wizardStep === "info" && (
                    <div className="space-y-5">
                      <div>
                        <h2 className="text-xl font-semibold text-[var(--foreground)]">
                          Thông tin gói kiến thức
                        </h2>
                        <p className="mt-1 text-sm text-[var(--muted-foreground)]">
                          Điền nhanh 5 trường cốt lõi để hệ thống hiểu đúng phạm vi bộ tài liệu.
                        </p>
                      </div>

                      <div className="space-y-3">
                        <input
                          value={packName}
                          onChange={(event) => setPackName(event.target.value)}
                          placeholder="Tên gói kiến thức"
                          className="w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--foreground)]/20"
                        />
                        <div className="grid gap-3 md:grid-cols-2">
                          <input
                            value={subject}
                            onChange={(event) => setSubject(event.target.value)}
                            placeholder="Chủ đề"
                            className="w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--foreground)]/20"
                          />
                          <input
                            value={curriculum}
                            onChange={(event) => setCurriculum(event.target.value)}
                            placeholder="Chương trình học"
                            className="w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--foreground)]/20"
                          />
                        </div>
                      </div>

                      <div className="rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4">
                        <div className="mb-3 text-sm font-medium text-[var(--foreground)]">
                          Mức độ khó
                        </div>
                        <div className="grid gap-2 md:grid-cols-3">
                          {DIFFICULTY_OPTIONS.map((option) => (
                            <button
                              key={option.value}
                              type="button"
                              onClick={() => setDifficulty(option.value)}
                              className={`rounded-2xl border px-4 py-3 text-left transition ${
                                difficulty === option.value
                                  ? "border-amber-300 bg-amber-50 text-amber-900"
                                  : "border-[var(--border)] bg-[var(--card)] text-[var(--foreground)]"
                              }`}
                            >
                              <div className="text-sm font-medium">{option.label}</div>
                              <div className="mt-1 text-xs text-[var(--muted-foreground)]">
                                {option.hint}
                              </div>
                            </button>
                          ))}
                        </div>
                      </div>

                      <textarea
                        value={learningObjectives}
                        onChange={(event) => setLearningObjectives(event.target.value)}
                        placeholder="Mục tiêu học tập, mỗi dòng một ý"
                        rows={5}
                        className="w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none transition focus:border-[var(--foreground)]/20"
                      />

                      <div className="flex items-center justify-between gap-3 rounded-2xl bg-[var(--muted)]/60 px-4 py-3">
                        <div className="text-sm text-[var(--muted-foreground)]">
                          Bước tiếp theo là tải tài liệu nguồn. Người dùng không cần chọn model hay provider.
                        </div>
                        <button
                          type="button"
                          disabled={!canContinueInfoStep}
                          onClick={() => setWizardStep("files")}
                          className="inline-flex items-center gap-2 rounded-full bg-[var(--foreground)] px-4 py-2 text-sm font-medium text-[var(--background)] disabled:cursor-not-allowed disabled:opacity-40"
                        >
                          Tiếp tục
                          <ArrowRight className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  )}

                  {wizardStep === "files" && (
                    <div className="space-y-5">
                      <div>
                        <h2 className="text-xl font-semibold text-[var(--foreground)]">Tài liệu</h2>
                        <p className="mt-1 text-sm text-[var(--muted-foreground)]">
                          Tải lên các tệp nguồn như `pdf`, `docx`, `pptx`, `txt`. Hệ thống sẽ dùng cấu hình lập chỉ mục mặc định ở backend.
                        </p>
                      </div>

                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="group flex min-h-56 w-full flex-col items-center justify-center rounded-[28px] border border-dashed border-[var(--border)] bg-[linear-gradient(180deg,rgba(255,255,255,0.92),rgba(248,244,238,0.96))] px-6 py-8 text-center transition hover:border-amber-300 hover:bg-amber-50/40"
                      >
                        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-amber-100 text-amber-700">
                          <Upload className="h-6 w-6" />
                        </div>
                        <div className="mt-4 text-base font-medium text-[var(--foreground)]">
                          Kéo thả tài liệu vào đây hoặc bấm để chọn tệp
                        </div>
                        <div className="mt-2 text-sm text-[var(--muted-foreground)]">
                          Giao diện upload được giữ theo kiểu các sản phẩm RAG hiện đại: gọn, rõ và ưu tiên trạng thái ingest.
                        </div>
                      </button>
                      <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        className="hidden"
                        onChange={(event) => setSelectedFiles(Array.from(event.target.files || []))}
                      />

                      <div className="space-y-2">
                        {selectedFiles.length ? (
                          selectedFiles.map((file) => (
                            <div
                              key={file.name}
                              className="flex items-center justify-between rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3"
                            >
                              <div className="min-w-0">
                                <div className="truncate text-sm font-medium text-[var(--foreground)]">
                                  {file.name}
                                </div>
                                <div className="mt-1 text-xs text-[var(--muted-foreground)]">
                                  {formatBytes(file.size)} • Sẵn sàng tải lên
                                </div>
                              </div>
                              <button
                                type="button"
                                onClick={() => removeSelectedFile(file.name)}
                                className="rounded-full border border-[var(--border)] p-2 text-[var(--muted-foreground)] transition hover:border-red-200 hover:bg-red-50 hover:text-red-600"
                              >
                                <Trash2 className="h-4 w-4" />
                              </button>
                            </div>
                          ))
                        ) : (
                          <div className="rounded-2xl border border-dashed border-[var(--border)] px-4 py-6 text-sm text-[var(--muted-foreground)]">
                            Chưa có tài liệu nào được chọn.
                          </div>
                        )}
                      </div>

                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <button
                          type="button"
                          onClick={() => setWizardStep("info")}
                          className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] px-4 py-2 text-sm text-[var(--foreground)]"
                        >
                          <ArrowLeft className="h-4 w-4" />
                          Quay lại
                        </button>
                        <button
                          type="button"
                          disabled={!canSubmitWizard}
                          onClick={() => void createKnowledgeBase()}
                          className="inline-flex items-center gap-2 rounded-full bg-[var(--foreground)] px-4 py-2 text-sm font-medium text-[var(--background)] disabled:cursor-not-allowed disabled:opacity-40"
                        >
                          {creating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
                          Tạo và lập chỉ mục
                        </button>
                      </div>
                    </div>
                  )}

                  {wizardStep === "done" && (
                    <div className="space-y-5">
                      <div>
                        <h2 className="text-xl font-semibold text-[var(--foreground)]">Hoàn tất</h2>
                        <p className="mt-1 text-sm text-[var(--muted-foreground)]">
                          Theo dõi tiến trình tổng quan ở trên và trạng thái từng tài liệu ở ngay bên dưới.
                        </p>
                      </div>

                      <div className="grid gap-3 md:grid-cols-3">
                        <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-4">
                          <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                            Tổng tài liệu
                          </div>
                          <div className="mt-2 text-2xl font-semibold text-[var(--foreground)]">
                            {summaryFileStatuses.length}
                          </div>
                        </div>
                        <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-4">
                          <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                            Đã lập chỉ mục
                          </div>
                          <div className="mt-2 text-2xl font-semibold text-[var(--foreground)]">
                            {indexedCount}
                          </div>
                        </div>
                        <div className="rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-4">
                          <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                            Trạng thái
                          </div>
                          <div className="mt-2 text-2xl font-semibold text-[var(--foreground)]">
                            {errorCount > 0
                              ? "Có lỗi"
                              : processingCount > 0
                                ? "Đang xử lý"
                                : "Hoàn tất"}
                          </div>
                        </div>
                      </div>

                      <div className="space-y-2 rounded-3xl border border-[var(--border)] bg-[var(--background)] p-4">
                        {summaryFileStatuses.length ? (
                          summaryFileStatuses.map((file) => (
                            <div
                              key={`${file.name}-${file.status}`}
                              className="flex items-center justify-between gap-3 rounded-2xl border border-[var(--border)] bg-[var(--card)] px-4 py-3"
                            >
                              <div className="min-w-0">
                                <div className="truncate text-sm font-medium text-[var(--foreground)]">
                                  {file.name}
                                </div>
                                {file.error ? (
                                  <div className="mt-1 text-xs text-red-600">{file.error}</div>
                                ) : (
                                  <div className="mt-1 text-xs text-[var(--muted-foreground)]">
                                    {file.updated_at || "Đang cập nhật trạng thái"}
                                  </div>
                                )}
                              </div>
                              <div
                                className={`rounded-full px-3 py-1 text-xs font-medium ${
                                  file.status === "indexed"
                                    ? "bg-emerald-50 text-emerald-700"
                                    : file.status === "error"
                                      ? "bg-red-50 text-red-700"
                                      : "bg-amber-50 text-amber-700"
                                }`}
                              >
                                {statusLabel(file.status)}
                              </div>
                            </div>
                          ))
                        ) : (
                          <div className="rounded-2xl border border-dashed border-[var(--border)] px-4 py-6 text-sm text-[var(--muted-foreground)]">
                            Chưa có tài liệu nào để hiển thị.
                          </div>
                        )}
                      </div>

                      {(createProcess.taskId || createProcess.logs.length > 0 || createProcess.executing) && (
                        <div className="space-y-2">
                          <div className="text-xs text-[var(--muted-foreground)]">
                            {createProcess.label}
                            {createProcess.taskId ? ` · ${createProcess.taskId}` : ""}
                          </div>
                          <ProcessLogs
                            logs={createProcess.logs}
                            executing={createProcess.executing}
                            title="Nhật ký xử lý"
                          />
                        </div>
                      )}

                      {createProcess.error && (
                        <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
                          {createProcess.error}
                        </div>
                      )}

                      <div className="flex flex-wrap gap-3">
                        <button
                          type="button"
                          onClick={() => setDetailPackName(activePackName)}
                          className="inline-flex items-center gap-2 rounded-full bg-[var(--foreground)] px-4 py-2 text-sm font-medium text-[var(--background)]"
                        >
                          Xem gói kiến thức
                        </button>
                        <button
                          type="button"
                          onClick={resetWizard}
                          className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] px-4 py-2 text-sm text-[var(--foreground)]"
                        >
                          Tạo gói mới
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </section>

              <aside className="rounded-[28px] border border-[var(--border)] bg-[linear-gradient(180deg,rgba(248,244,238,0.94),rgba(255,255,255,0.98))] p-6 shadow-sm">
                <div className="flex items-center gap-2 text-sm font-medium text-[var(--foreground)]">
                  <FileText className="h-4 w-4 text-amber-600" />
                  Bảng trạng thái ingest
                </div>
                <div className="mt-3 text-sm text-[var(--muted-foreground)]">
                  Bảng này luôn phản ánh gói đang tạo hoặc gói bạn vừa chọn từ danh sách phía dưới.
                </div>

                {activeSummary ? (
                  <div className="mt-6 space-y-4">
                    <div className="rounded-3xl border border-[var(--border)] bg-[var(--card)] p-4">
                      <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                        Gói đang theo dõi
                      </div>
                      <div className="mt-2 text-xl font-semibold text-[var(--foreground)]">
                        {activeSummary.name}
                      </div>
                      <div className="mt-4 grid gap-3">
                        <div className="rounded-2xl bg-[var(--background)] px-4 py-3">
                          <div className="text-xs text-[var(--muted-foreground)]">Chủ đề</div>
                          <div className="mt-1 text-sm font-medium text-[var(--foreground)]">
                            {activeSummary.subject || "Chưa chọn"}
                          </div>
                        </div>
                        <div className="rounded-2xl bg-[var(--background)] px-4 py-3">
                          <div className="text-xs text-[var(--muted-foreground)]">Mức độ khó</div>
                          <div className="mt-1 text-sm font-medium text-[var(--foreground)]">
                            {difficultyLabel(activeSummary.difficulty)}
                          </div>
                        </div>
                        <div className="rounded-2xl bg-[var(--background)] px-4 py-3">
                          <div className="text-xs text-[var(--muted-foreground)]">Chương trình học</div>
                          <div className="mt-1 text-sm font-medium text-[var(--foreground)]">
                            {activeSummary.curriculum}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] px-4 py-4">
                        <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                          Số tài liệu
                        </div>
                        <div className="mt-2 text-2xl font-semibold text-[var(--foreground)]">
                          {activeSummary.documentCount}
                        </div>
                      </div>
                      <div className="rounded-2xl border border-[var(--border)] bg-[var(--card)] px-4 py-4">
                        <div className="text-xs uppercase tracking-[0.18em] text-[var(--muted-foreground)]">
                          Trạng thái index
                        </div>
                        <div className="mt-2 text-2xl font-semibold text-[var(--foreground)]">
                          {statusLabel(activeSummary.status)}
                        </div>
                      </div>
                    </div>

                    <div className="rounded-3xl border border-[var(--border)] bg-[var(--card)] p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <div className="text-sm font-medium text-[var(--foreground)]">
                            Tiến trình tổng quan
                          </div>
                          <div className="mt-1 text-xs text-[var(--muted-foreground)]">
                            {progressSummaryLabel(activeSummary.progress)}
                          </div>
                        </div>
                        <div className="text-sm font-semibold text-[var(--foreground)]">
                          {progressPercent(activeSummary.progress)}%
                        </div>
                      </div>
                      <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--border)]">
                        <div
                          className="h-full rounded-full bg-[linear-gradient(90deg,#e7a658,#d97706)] transition-all"
                          style={{ width: `${progressPercent(activeSummary.progress)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="mt-6 rounded-3xl border border-dashed border-[var(--border)] px-5 py-10 text-center text-sm text-[var(--muted-foreground)]">
                    Điền thông tin ở wizard hoặc bấm `Xem chi tiết` trên một gói hiện có để xem trạng thái ở đây.
                  </div>
                )}
              </aside>
            </div>

            <section className="rounded-[28px] border border-[var(--border)] bg-[var(--card)] p-6 shadow-sm">
              <div className="flex items-center gap-2 text-sm font-medium text-[var(--foreground)]">
                <BookOpen className="h-4 w-4 text-amber-600" />
                Danh sách gói kiến thức
              </div>
              <div className="mt-5 space-y-4">
                {combinedKbs.length ? (
                  combinedKbs.map((kb) => {
                    const progress = kb.progress;
                    const currentDifficulty = kb.metadata?.difficulty ?? kb.metadata?.grade ?? null;
                    return (
                      <div
                        key={kb.name}
                        className="rounded-[24px] border border-[var(--border)] bg-[var(--background)] p-4"
                      >
                        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                          <div className="min-w-0">
                            <div className="flex flex-wrap items-center gap-2">
                              <h3 className="text-lg font-semibold text-[var(--foreground)]">
                                {kb.name}
                              </h3>
                              {kb.is_default && (
                                <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
                                  Mặc định
                                </span>
                              )}
                            </div>
                            <div className="mt-3 flex flex-wrap gap-2">
                              <span className="rounded-full bg-[var(--card)] px-3 py-1 text-xs text-[var(--muted-foreground)]">
                                Chủ đề: {kb.metadata?.subject || "Chưa có"}
                              </span>
                              <span className="rounded-full bg-[var(--card)] px-3 py-1 text-xs text-[var(--muted-foreground)]">
                                Mức độ khó: {difficultyLabel(currentDifficulty)}
                              </span>
                              <span className="rounded-full bg-[var(--card)] px-3 py-1 text-xs text-[var(--muted-foreground)]">
                                Chương trình học: {kb.metadata?.curriculum || "Chưa có"}
                              </span>
                              <span className="rounded-full bg-[var(--card)] px-3 py-1 text-xs text-[var(--muted-foreground)]">
                                Số tài liệu: {kb.statistics?.raw_documents ?? 0}
                              </span>
                              <span className="rounded-full bg-[var(--card)] px-3 py-1 text-xs text-[var(--muted-foreground)]">
                                Trạng thái index: {statusLabel(progress?.stage ?? kb.status)}
                              </span>
                            </div>
                          </div>

                          <div className="flex flex-wrap gap-2">
                            <button
                              type="button"
                              onClick={() => setDetailPackName(kb.name)}
                              className="rounded-full border border-[var(--border)] px-4 py-2 text-sm text-[var(--foreground)]"
                            >
                              Xem chi tiết
                            </button>
                            <button
                              type="button"
                              onClick={() => startEditKnowledgePack(kb)}
                              className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] px-4 py-2 text-sm text-[var(--foreground)]"
                            >
                              <PencilLine className="h-4 w-4" />
                              Chỉnh sửa
                            </button>
                            <button
                              type="button"
                              onClick={() => void deleteKnowledgeBase(kb.name)}
                              className="inline-flex items-center gap-2 rounded-full border border-red-200 px-4 py-2 text-sm text-red-700"
                            >
                              <Trash2 className="h-4 w-4" />
                              Xóa
                            </button>
                          </div>
                        </div>

                        {progress && (
                          <div className="mt-4 rounded-2xl border border-[var(--border)] bg-[var(--card)] px-4 py-3">
                            <div className="flex items-center justify-between gap-3">
                              <div className="text-sm text-[var(--foreground)]">
                                {progressSummaryLabel(progress)}
                              </div>
                              <div className="text-sm font-medium text-[var(--foreground)]">
                                {progressPercent(progress)}%
                              </div>
                            </div>
                            <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--border)]">
                              <div
                                className="h-full rounded-full bg-[linear-gradient(90deg,#e7a658,#d97706)] transition-all"
                                style={{ width: `${progressPercent(progress)}%` }}
                              />
                            </div>
                          </div>
                        )}

                        {editingKbName === kb.name && (
                          <div className="mt-4 rounded-[24px] border border-[var(--border)] bg-[var(--card)] p-4">
                            <div className="mb-4 text-sm font-medium text-[var(--foreground)]">
                              Chỉnh sửa gói kiến thức
                            </div>
                            <div className="grid gap-3 md:grid-cols-2">
                              <input
                                value={editSubject}
                                onChange={(event) => setEditSubject(event.target.value)}
                                placeholder="Chủ đề"
                                className="rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none"
                              />
                              <input
                                value={editCurriculum}
                                onChange={(event) => setEditCurriculum(event.target.value)}
                                placeholder="Chương trình học"
                                className="rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none"
                              />
                            </div>
                            <div className="mt-3 grid gap-2 md:grid-cols-3">
                              {DIFFICULTY_OPTIONS.map((option) => (
                                <button
                                  key={option.value}
                                  type="button"
                                  onClick={() => setEditDifficulty(option.value)}
                                  className={`rounded-2xl border px-4 py-3 text-left text-sm ${
                                    editDifficulty === option.value
                                      ? "border-amber-300 bg-amber-50 text-amber-900"
                                      : "border-[var(--border)] bg-[var(--background)] text-[var(--foreground)]"
                                  }`}
                                >
                                  {option.label}
                                </button>
                              ))}
                            </div>
                            <textarea
                              value={editLearningObjectives}
                              onChange={(event) => setEditLearningObjectives(event.target.value)}
                              placeholder="Mục tiêu học tập, mỗi dòng một ý"
                              rows={4}
                              className="mt-3 w-full rounded-2xl border border-[var(--border)] bg-[var(--background)] px-4 py-3 text-sm text-[var(--foreground)] outline-none"
                            />
                            {editError && (
                              <div className="mt-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                                {editError}
                              </div>
                            )}
                            <div className="mt-4 flex flex-wrap gap-3">
                              <button
                                type="button"
                                disabled={savingMetadata}
                                onClick={() => void saveKnowledgePackMetadata()}
                                className="inline-flex items-center gap-2 rounded-full bg-[var(--foreground)] px-4 py-2 text-sm font-medium text-[var(--background)] disabled:cursor-not-allowed disabled:opacity-40"
                              >
                                {savingMetadata ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle2 className="h-4 w-4" />}
                                Lưu thay đổi
                              </button>
                              <button
                                type="button"
                                onClick={() => setEditingKbName(null)}
                                className="rounded-full border border-[var(--border)] px-4 py-2 text-sm text-[var(--foreground)]"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <div className="rounded-[24px] border border-dashed border-[var(--border)] px-6 py-12 text-center">
                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-[var(--muted)]">
                      <AlertCircle className="h-5 w-5 text-[var(--muted-foreground)]" />
                    </div>
                    <div className="mt-4 text-base font-medium text-[var(--foreground)]">
                      Chưa có gói kiến thức nào
                    </div>
                    <div className="mt-2 text-sm text-[var(--muted-foreground)]">
                      Bắt đầu bằng wizard phía trên để tải bộ tài liệu đầu tiên cho lớp học.
                    </div>
                  </div>
                )}
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  );
}
