from __future__ import annotations

from typing import Literal, TypedDict


ObservationSource = Literal["assessment", "tutoring"]
DiagnosisType = Literal["concept_gap", "careless_error", "low_confidence", "needs_scaffold"]
ConfidenceTag = Literal["low", "medium", "high"]
SupportLevel = Literal["independent", "guided", "intensive"]
ConfidenceTrend = Literal["up", "flat", "down"]


class ObservationRecord(TypedDict):
    observation_id: str
    session_id: str
    student_id: str
    source: ObservationSource
    topic: str
    question_id: str
    is_correct: bool
    latency_seconds: int | None
    hint_count: int
    retry_count: int
    dominant_error: DiagnosisType | None


class StudentStateRecord(TypedDict):
    student_id: str
    repeated_mistakes: list[str]
    support_level: SupportLevel
    confidence_trend: ConfidenceTrend


class DiagnosisRecord(TypedDict):
    diagnosis_type: DiagnosisType
    confidence_tag: ConfidenceTag
    topic: str
    evidence: list[str]


class RecommendationRecord(TypedDict):
    action_id: str
    action_type: Literal[
        "review_prerequisite",
        "retry_easier",
        "increase_scaffold",
        "small_group_support",
    ]
    target_student_ids: list[str]
    topic: str
    rationale: str
