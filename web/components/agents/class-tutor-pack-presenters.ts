import type { AgentSpecDetail } from "../../lib/agent-spec-api";
import type { KnowledgeBaseSummary } from "../../lib/knowledge-api";

export interface TutorPackFlowLabels {
  noPackLinked: string;
  packNotFound: string;
  noSubject: string;
  noDifficulty: string;
  noObjectives: string;
  noLanguage: string;
  noTone: string;
  noTeachingStyle: string;
  noEscalation: string;
  linkedStatus: string;
  unlinkedStatus: string;
  missingStatus: string;
  objectiveCount: (count: number) => string;
}

export interface TutorPackFlowViewModel {
  packName: string;
  subject: string;
  difficulty: string;
  language: string;
  tone: string;
  objectiveSummary: string;
  teachingPromise: string;
  escalationSummary: string;
  statusLabel: string;
  statusTone: "linked" | "unlinked" | "missing";
  linkedPackExists: boolean;
}

function cleanText(value: string | null | undefined): string {
  return value?.trim() || "";
}

function chooseFirstSentence(value: string, fallback: string): string {
  const normalized = cleanText(value).replace(/\s+/g, " ");
  if (!normalized) {
    return fallback;
  }
  const [firstSentence] = normalized.split(/(?<=[.!?])\s+/);
  return firstSentence || normalized;
}

export function buildTutorPackOptions(knowledgeBases: KnowledgeBaseSummary[]): Array<{ value: string; label: string }> {
  return knowledgeBases
    .map((item) => ({ value: item.name, label: item.name }))
    .sort((left, right) => left.label.localeCompare(right.label));
}

export function buildTutorPackFlowViewModel(
  draft: Pick<AgentSpecDetail, "linked_knowledge_pack" | "structured">,
  knowledgeBases: KnowledgeBaseSummary[],
  labels: TutorPackFlowLabels,
): TutorPackFlowViewModel {
  const linkedPackName = cleanText(draft.linked_knowledge_pack);
  const linkedPack = linkedPackName
    ? knowledgeBases.find((item) => item.name === linkedPackName) ?? null
    : null;
  const objectives = linkedPack?.metadata?.learning_objectives?.filter((item): item is string => Boolean(item?.trim())) ?? [];
  const subject = cleanText(linkedPack?.metadata?.subject) || cleanText(draft.structured.identity.subject) || labels.noSubject;
  const difficulty = cleanText(linkedPack?.metadata?.difficulty) || labels.noDifficulty;
  const language = cleanText(draft.structured.identity.primary_language) || cleanText(linkedPack?.metadata?.language) || labels.noLanguage;
  const tone = cleanText(draft.structured.identity.tone) || labels.noTone;
  const teachingPromise = chooseFirstSentence(draft.structured.soul.teaching_philosophy, labels.noTeachingStyle);
  const escalationSummary = chooseFirstSentence(draft.structured.rules.escalation_rule || draft.structured.rules.guardrails, labels.noEscalation);

  if (!linkedPackName) {
    return {
      packName: labels.noPackLinked,
      subject,
      difficulty,
      language,
      tone,
      objectiveSummary: labels.noObjectives,
      teachingPromise,
      escalationSummary,
      statusLabel: labels.unlinkedStatus,
      statusTone: "unlinked",
      linkedPackExists: false,
    };
  }

  if (!linkedPack) {
    return {
      packName: linkedPackName,
      subject,
      difficulty,
      language,
      tone,
      objectiveSummary: labels.noObjectives,
      teachingPromise,
      escalationSummary,
      statusLabel: labels.missingStatus,
      statusTone: "missing",
      linkedPackExists: false,
    };
  }

  return {
    packName: linkedPack.name,
    subject,
    difficulty,
    language,
    tone,
    objectiveSummary: objectives.length > 0 ? labels.objectiveCount(objectives.length) : labels.noObjectives,
    teachingPromise,
    escalationSummary,
    statusLabel: labels.linkedStatus,
    statusTone: "linked",
    linkedPackExists: true,
  };
}
