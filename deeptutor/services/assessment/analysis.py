from __future__ import annotations

import re
from typing import Any

_TOPIC_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "is",
    "are",
    "what",
    "which",
    "solve",
    "find",
    "calculate",
    "determine",
}


def infer_topic_from_question(question: str, fallback: str = "general") -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", question.lower())
    filtered = [w for w in words if w not in _TOPIC_STOPWORDS]
    if not filtered:
        return fallback
    return " ".join(filtered[:2])


def build_assessment_analysis(review: dict[str, Any]) -> dict[str, Any]:
    results = review.get("results", [])
    if not isinstance(results, list):
        results = []

    topic_buckets: dict[str, dict[str, int]] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question") or "")
        topic = infer_topic_from_question(question)
        bucket = topic_buckets.setdefault(topic, {"total": 0, "correct": 0, "incorrect": 0})
        bucket["total"] += 1
        if bool(item.get("is_correct")):
            bucket["correct"] += 1
        else:
            bucket["incorrect"] += 1

    performance_by_topic = []
    for topic, counts in sorted(topic_buckets.items(), key=lambda kv: (-kv[1]["incorrect"], kv[0])):
        total = counts["total"]
        accuracy = round((counts["correct"] / total) * 100) if total else 0
        performance_by_topic.append(
            {
                "topic": topic,
                "total_questions": total,
                "correct_count": counts["correct"],
                "incorrect_count": counts["incorrect"],
                "accuracy_percent": accuracy,
            }
        )

    weak_topics = [row["topic"] for row in performance_by_topic if row["incorrect_count"] > 0][:3]
    strong_topics = [row["topic"] for row in performance_by_topic if row["accuracy_percent"] >= 80][:3]

    score_percent = int(review.get("summary", {}).get("score_percent", 0))
    recommendations: list[str] = []
    if weak_topics:
        recommendations.append(f"Review these topics first: {', '.join(weak_topics)}.")
    if score_percent < 75:
        recommendations.append("Retry a focused quiz on weak topics before moving on.")
    elif score_percent < 90:
        recommendations.append("Practice mixed-difficulty questions to improve consistency.")
    else:
        recommendations.append("You are ready for advanced questions and extension material.")
    if strong_topics:
        recommendations.append(f"Strong areas: {', '.join(strong_topics)}.")

    return {
        "session_id": review.get("session_id"),
        "summary": review.get("summary", {}),
        "performance_by_topic": performance_by_topic,
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "recommendations": recommendations,
    }
