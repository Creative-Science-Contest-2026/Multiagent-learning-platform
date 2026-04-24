"""Deterministic learning-path suggestions for dashboard progress flows."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from deeptutor.knowledge.manager import KnowledgeBaseManager
from deeptutor.services.config import PROJECT_ROOT

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS = {"and", "for", "the", "with", "from", "into", "topic"}
_KB_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_bases"


def _tokenize(value: str) -> set[str]:
    return {
        token
        for token in _TOKEN_RE.findall(value.lower())
        if len(token) > 2 and token not in _STOPWORDS
    }


def _topic_matches(left: str, right: str) -> bool:
    left_tokens = _tokenize(left)
    right_tokens = _tokenize(right)
    if not left_tokens or not right_tokens:
        return left.strip().lower() == right.strip().lower()
    overlap = left_tokens & right_tokens
    return bool(overlap) and (len(overlap) >= 2 or left.strip().lower() in right.strip().lower() or right.strip().lower() in left.strip().lower())


def _get_kb_manager() -> KnowledgeBaseManager:
    return KnowledgeBaseManager(base_dir=str(Path(_KB_BASE_DIR)))


def build_suggested_learning_path(
    *,
    focus_topics: list[dict[str, Any]],
    mastered_topics: list[dict[str, Any]],
    knowledge_bases: list[str],
) -> list[dict[str, Any]]:
    suggestions: list[dict[str, Any]] = []
    seen_topics: set[str] = set()
    mastered_names = [str(row.get("topic") or "") for row in mastered_topics]

    def add_suggestion(topic: str, *, status: str, source: str, knowledge_base: str | None = None) -> None:
        normalized = topic.strip()
        if not normalized:
            return
        key = normalized.lower()
        if key in seen_topics:
            return
        seen_topics.add(key)
        payload = {
            "topic": normalized,
            "status": status,
            "source": source,
        }
        if knowledge_base:
            payload["knowledge_base"] = knowledge_base
        suggestions.append(payload)

    for topic in focus_topics:
        add_suggestion(
            str(topic.get("topic") or ""),
            status="review",
            source="focus_topic",
        )

    kb_manager = _get_kb_manager()
    for kb_name in knowledge_bases:
        metadata = kb_manager.get_metadata(kb_name)
        objectives = metadata.get("learning_objectives") if isinstance(metadata, dict) else None
        if not isinstance(objectives, list):
            continue
        for objective in objectives:
            if not isinstance(objective, str) or not objective.strip():
                continue
            if any(_topic_matches(objective, mastered) for mastered in mastered_names):
                continue
            add_suggestion(
                objective,
                status="next",
                source="learning_objective",
                knowledge_base=kb_name,
            )

    return suggestions[:5]
