import { describe, expect, it } from "vitest";

import {
  buildTutorPackFlowViewModel,
  buildTutorPackOptions,
} from "../components/agents/class-tutor-pack-presenters";
import type { AgentSpecDetail } from "../lib/agent-spec-api";
import type { KnowledgeBaseSummary } from "../lib/knowledge-api";

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

describe("class tutor pack presenters", () => {
  it("sorts pack names for the selector", () => {
    const options = buildTutorPackOptions([
      { name: "z-pack" },
      { name: "algebra-pack" },
    ] satisfies KnowledgeBaseSummary[]);

    expect(options).toEqual([
      { value: "algebra-pack", label: "algebra-pack" },
      { value: "z-pack", label: "z-pack" },
    ]);
  });

  it("reflects a linked knowledge pack", () => {
    const draft = buildDraft({ linked_knowledge_pack: "fractions-pack" });
    const knowledgeBases: KnowledgeBaseSummary[] = [
      {
        name: "fractions-pack",
        metadata: {
          subject: "Toán",
          difficulty: "beginner",
          language: "Tiếng Việt",
          learning_objectives: [
            "Hiểu khái niệm phân số",
            "So sánh phân số",
            "Rút gọn phân số",
          ],
        },
      },
    ];

    const viewModel = buildTutorPackFlowViewModel(draft, knowledgeBases, labels);

    expect(viewModel.packName).toBe("fractions-pack");
    expect(viewModel.statusTone).toBe("linked");
    expect(viewModel.statusLabel).toBe("Đã gắn");
    expect(viewModel.subject).toBe("Toán");
    expect(viewModel.difficulty).toBe("beginner");
    expect(viewModel.language).toBe("Tiếng Việt");
    expect(viewModel.objectiveSummary).toBe("3 mục tiêu trọng tâm");
    expect(viewModel.teachingPromise).toBe(
      "Giúp học sinh hiểu bản chất trước khi làm nhanh.",
    );
    expect(viewModel.escalationSummary).toBe(
      "Nếu học sinh lặp lại cùng một lỗi sau nhiều gợi ý thì chuyển giáo viên xem lại.",
    );
  });

  it("shows unlinked state without a selected pack", () => {
    const viewModel = buildTutorPackFlowViewModel(buildDraft(), [], labels);

    expect(viewModel.packName).toBe("Chưa gắn gói kiến thức");
    expect(viewModel.statusTone).toBe("unlinked");
    expect(viewModel.statusLabel).toBe("Chưa gắn");
    expect(viewModel.subject).toBe("Toán");
    expect(viewModel.objectiveSummary).toBe("Chưa có mục tiêu học tập");
  });

  it("marks missing pack when the saved link no longer exists", () => {
    const viewModel = buildTutorPackFlowViewModel(
      buildDraft({ linked_knowledge_pack: "fractions-pack" }),
      [],
      labels,
    );

    expect(viewModel.packName).toBe("fractions-pack");
    expect(viewModel.statusTone).toBe("missing");
    expect(viewModel.statusLabel).toBe("Gói đã bị thiếu");
    expect(viewModel.linkedPackExists).toBe(false);
  });
});
