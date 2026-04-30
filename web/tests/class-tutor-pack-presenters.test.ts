import test from "node:test";
import assert from "node:assert/strict";

import { buildTutorPackFlowViewModel, buildTutorPackOptions } from "../components/agents/class-tutor-pack-presenters.ts";
import type { AgentSpecDetail } from "../lib/agent-spec-api.ts";
import type { KnowledgeBaseSummary } from "../lib/knowledge-api.ts";

const labels = {
  noPackLinked: "Chưa gắn gói kiến thức",
  packNotFound: "Không tìm thấy gói kiến thức",
  noSubject: "Chưa có môn học",
  noDifficulty: "Chưa có mức độ",
  noObjectives: "Chưa có mục tiêu học tập",
  noLanguage: "Chưa có ngôn ngữ",
  noTone: "Chưa có giọng điệu",
  noTeachingStyle: "Chưa mô tả cách gia sư sẽ hỗ trợ",
  noEscalation: "Chưa có quy tắc chuyển giáo viên xem lại",
  linkedStatus: "Đã gắn",
  unlinkedStatus: "Chưa gắn",
  missingStatus: "Gói đã bị thiếu",
  objectiveCount: (count: number) => `${count} mục tiêu trọng tâm`,
};

function buildDraft(overrides?: Partial<AgentSpecDetail>): AgentSpecDetail {
  return {
    agent_id: "fraction-coach",
    display_name: "Gia sư phân số",
    description: "",
    linked_knowledge_pack: null,
    version: 1,
    files: {},
    structured: {
      identity: {
        agent_name: "Gia sư phân số",
        subject: "Toán",
        grade_band: "Lớp 6",
        tone: "Bình tĩnh và khích lệ",
        primary_language: "Tiếng Việt",
        persona_summary: "",
      },
      soul: {
        teaching_philosophy: "Giúp học sinh hiểu bản chất trước khi làm nhanh. Luôn đi từ ví dụ gần gũi.",
        when_student_wrong: "",
        when_student_stuck: "",
        encouragement_style: "",
      },
      rules: {
        do_not_solve_directly: "yes",
        max_session_minutes: "",
        hint_policy: "",
        escalation_rule: "Nếu học sinh lặp lại cùng một lỗi sau nhiều gợi ý thì chuyển giáo viên xem lại.",
        guardrails: "",
      },
    },
    summary: {
      subject: "",
      language: "",
      teaching_philosophy: "",
      guardrails: "",
    },
    ...overrides,
  };
}

test("buildTutorPackOptions sorts pack names for the selector", () => {
  const options = buildTutorPackOptions([
    { name: "z-pack" },
    { name: "algebra-pack" },
  ] satisfies KnowledgeBaseSummary[]);

  assert.deepEqual(options, [
    { value: "algebra-pack", label: "algebra-pack" },
    { value: "z-pack", label: "z-pack" },
  ]);
});

test("buildTutorPackFlowViewModel reflects a linked knowledge pack", () => {
  const draft = buildDraft({ linked_knowledge_pack: "fractions-pack" });
  const knowledgeBases: KnowledgeBaseSummary[] = [
    {
      name: "fractions-pack",
      metadata: {
        subject: "Toán",
        difficulty: "beginner",
        language: "Tiếng Việt",
        learning_objectives: ["Hiểu khái niệm phân số", "So sánh phân số", "Rút gọn phân số"],
      },
    },
  ];

  const viewModel = buildTutorPackFlowViewModel(draft, knowledgeBases, labels);

  assert.equal(viewModel.packName, "fractions-pack");
  assert.equal(viewModel.statusTone, "linked");
  assert.equal(viewModel.statusLabel, "Đã gắn");
  assert.equal(viewModel.subject, "Toán");
  assert.equal(viewModel.difficulty, "beginner");
  assert.equal(viewModel.language, "Tiếng Việt");
  assert.equal(viewModel.objectiveSummary, "3 mục tiêu trọng tâm");
  assert.equal(viewModel.teachingPromise, "Giúp học sinh hiểu bản chất trước khi làm nhanh.");
  assert.equal(viewModel.escalationSummary, "Nếu học sinh lặp lại cùng một lỗi sau nhiều gợi ý thì chuyển giáo viên xem lại.");
});

test("buildTutorPackFlowViewModel shows unlinked state without a selected pack", () => {
  const viewModel = buildTutorPackFlowViewModel(buildDraft(), [], labels);

  assert.equal(viewModel.packName, "Chưa gắn gói kiến thức");
  assert.equal(viewModel.statusTone, "unlinked");
  assert.equal(viewModel.statusLabel, "Chưa gắn");
  assert.equal(viewModel.subject, "Toán");
  assert.equal(viewModel.objectiveSummary, "Chưa có mục tiêu học tập");
});

test("buildTutorPackFlowViewModel marks missing pack when the saved link no longer exists", () => {
  const viewModel = buildTutorPackFlowViewModel(
    buildDraft({ linked_knowledge_pack: "fractions-pack" }),
    [],
    labels,
  );

  assert.equal(viewModel.packName, "fractions-pack");
  assert.equal(viewModel.statusTone, "missing");
  assert.equal(viewModel.statusLabel, "Gói đã bị thiếu");
  assert.equal(viewModel.linkedPackExists, false);
});
