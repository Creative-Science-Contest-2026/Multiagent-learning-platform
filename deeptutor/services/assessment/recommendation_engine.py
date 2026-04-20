from __future__ import annotations

from collections import Counter
from typing import Any

from deeptutor.services.assessment.analysis import build_assessment_analysis


def _unique_kbs(rows: list[dict[str, Any]]) -> list[str]:
    return sorted({kb for row in rows for kb in row.get("knowledge_bases", [])})


def recommend_next_assessment(
    assessment_rows: list[dict[str, Any]],
    *,
    preferred_session_id: str | None = None,
) -> dict[str, Any]:
    if not assessment_rows:
        return {
            "status": "insufficient-data",
            "recommended_topic": None,
            "suggested_action": "complete-assessment",
            "recommended_knowledge_bases": [],
            "source_session_ids": [],
            "reason": "Complete at least one assessment to unlock recommendations.",
            "history_summary": {
                "assessments_considered": 0,
                "average_score_percent": 0,
                "weak_topics": [],
                "strong_topics": [],
            },
        }

    ordered_rows = sorted(assessment_rows, key=lambda row: row.get("timestamp", 0), reverse=True)
    if preferred_session_id:
        ordered_rows.sort(key=lambda row: row.get("session_id") != preferred_session_id)

    topic_stats: dict[str, dict[str, Any]] = {}
    weak_topic_hits: Counter[str] = Counter()
    strong_topic_hits: Counter[str] = Counter()
    average_score_percent = round(
        sum(int(row.get("summary", {}).get("score_percent", 0)) for row in ordered_rows) / len(ordered_rows)
    )

    for row in ordered_rows:
        analysis = build_assessment_analysis(
            {
                "session_id": row.get("session_id"),
                "summary": row.get("summary") or {},
                "results": row.get("assessment_results") or [],
            }
        )
        for topic_row in analysis["performance_by_topic"]:
            topic = topic_row["topic"]
            current = topic_stats.setdefault(
                topic,
                {
                    "topic": topic,
                    "incorrect_count": 0,
                    "correct_count": 0,
                    "total_questions": 0,
                    "accuracy_percent": 0,
                    "knowledge_bases": set(),
                },
            )
            current["incorrect_count"] += topic_row["incorrect_count"]
            current["correct_count"] += topic_row["correct_count"]
            current["total_questions"] += topic_row["total_questions"]
            current["knowledge_bases"].update(row.get("knowledge_bases", []))
            total = current["total_questions"]
            current["accuracy_percent"] = round((current["correct_count"] / total) * 100) if total else 0

        weak_topic_hits.update(analysis["weak_topics"])
        strong_topic_hits.update(analysis["strong_topics"])

    weak_topic = None
    if topic_stats:
        weak_candidates = [row for row in topic_stats.values() if row["incorrect_count"] > 0]
        if weak_candidates:
            weak_topic = sorted(
                weak_candidates,
                key=lambda row: (-row["incorrect_count"], row["accuracy_percent"], row["topic"]),
            )[0]

    strong_topic = None
    if topic_stats:
        strong_candidates = [row for row in topic_stats.values() if row["accuracy_percent"] >= 80]
        if strong_candidates:
            strong_topic = sorted(
                strong_candidates,
                key=lambda row: (-row["accuracy_percent"], row["topic"]),
            )[0]

    if weak_topic is not None:
        return {
            "status": "ready",
            "recommended_topic": weak_topic["topic"],
            "suggested_action": "retry-focused-quiz" if average_score_percent < 75 else "mixed-practice",
            "recommended_knowledge_bases": sorted(weak_topic["knowledge_bases"]),
            "source_session_ids": [str(row["session_id"]) for row in ordered_rows],
            "reason": (
                f"Recent assessments show the most missed questions in {weak_topic['topic']}, "
                f"so the next assessment should revisit that area first."
            ),
            "history_summary": {
                "assessments_considered": len(ordered_rows),
                "average_score_percent": average_score_percent,
                "weak_topics": [topic for topic, _count in weak_topic_hits.most_common(3)],
                "strong_topics": [topic for topic, _count in strong_topic_hits.most_common(3)],
            },
        }

    if strong_topic is not None:
        return {
            "status": "ready",
            "recommended_topic": strong_topic["topic"],
            "suggested_action": "advance-challenge",
            "recommended_knowledge_bases": sorted(strong_topic["knowledge_bases"]),
            "source_session_ids": [str(row["session_id"]) for row in ordered_rows],
            "reason": (
                f"Recent assessments are consistently strong in {strong_topic['topic']}, "
                f"so the next assessment can increase difficulty."
            ),
            "history_summary": {
                "assessments_considered": len(ordered_rows),
                "average_score_percent": average_score_percent,
                "weak_topics": [topic for topic, _count in weak_topic_hits.most_common(3)],
                "strong_topics": [topic for topic, _count in strong_topic_hits.most_common(3)],
            },
        }

    return {
        "status": "ready",
        "recommended_topic": "general review",
        "suggested_action": "skill-check",
        "recommended_knowledge_bases": _unique_kbs(ordered_rows),
        "source_session_ids": [str(row["session_id"]) for row in ordered_rows],
        "reason": "Recent assessments do not show a clear weak topic, so a balanced review quiz is the safest next step.",
        "history_summary": {
            "assessments_considered": len(ordered_rows),
            "average_score_percent": average_score_percent,
            "weak_topics": [topic for topic, _count in weak_topic_hits.most_common(3)],
            "strong_topics": [topic for topic, _count in strong_topic_hits.most_common(3)],
        },
    }
