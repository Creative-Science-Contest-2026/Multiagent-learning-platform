"""Compile teacher-authored spec slices into a runtime policy contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from deeptutor.core.context import UnifiedContext

SLICE_NAMES = ["SOUL", "RULES", "WORKFLOW", "ASSESSMENT", "KNOWLEDGE", "CURRICULUM"]
SOURCE_PRIORITY = [
    "teacher_kb",
    "curriculum_excerpt",
    "teacher_rules",
    "llm_prior_knowledge",
]
DEFAULT_KNOWLEDGE_POLICY = "kb_preferred"


@dataclass
class RuntimePolicy:
    """Serializable policy object injected into runtime context."""

    capability: str
    slices: dict[str, str]
    sources: dict[str, str]
    knowledge_policy: str
    source_priority: list[str]

    def to_dict(self) -> dict[str, Any]:
        applied = [name for name, value in self.slices.items() if value.strip()]
        missing = [name for name in SLICE_NAMES if name not in applied]
        return {
            "capability": self.capability,
            "slices": dict(self.slices),
            "sources": dict(self.sources),
            "knowledge_policy": self.knowledge_policy,
            "source_priority": list(self.source_priority),
            "debug": {
                "applied_slices": applied,
                "missing_slices": missing,
            },
        }


def ensure_runtime_policy(context: UnifiedContext, capability: str) -> RuntimePolicy:
    """Return existing compiled policy from context metadata or compile one."""
    existing = context.metadata.get("runtime_policy")
    if isinstance(existing, dict):
        return RuntimePolicy(
            capability=str(existing.get("capability") or capability),
            slices={k: str(v or "") for k, v in dict(existing.get("slices") or {}).items()},
            sources={k: str(v or "") for k, v in dict(existing.get("sources") or {}).items()},
            knowledge_policy=str(existing.get("knowledge_policy") or DEFAULT_KNOWLEDGE_POLICY),
            source_priority=list(existing.get("source_priority") or SOURCE_PRIORITY),
        )

    policy = _compile_runtime_policy(context=context, capability=capability)
    context.metadata["runtime_policy"] = policy.to_dict()
    return policy


def format_chat_system_context(policy: RuntimePolicy) -> str:
    """Build tutoring-oriented system guidance from assembled slices."""
    blocks: list[str] = [
        "Teacher Runtime Policy:",
        _slice_block("SOUL", policy.slices.get("SOUL", "")),
        _slice_block("RULES", policy.slices.get("RULES", "")),
        _slice_block("WORKFLOW", policy.slices.get("WORKFLOW", "")),
        _slice_block("KNOWLEDGE", policy.slices.get("KNOWLEDGE", "")),
        "Knowledge source priority:",
        " > ".join(policy.source_priority),
        "Scope guardrail: Stay within teacher-defined scope and clarify uncertainty when evidence is missing.",
    ]
    return "\n\n".join(block for block in blocks if block.strip())


def format_assessment_context(policy: RuntimePolicy) -> str:
    """Build assessment-oriented guidance from assembled slices."""
    blocks: list[str] = [
        "Teacher Assessment Runtime Policy:",
        _slice_block("ASSESSMENT", policy.slices.get("ASSESSMENT", "")),
        _slice_block("RULES", policy.slices.get("RULES", "")),
        _slice_block("WORKFLOW", policy.slices.get("WORKFLOW", "")),
        _slice_block("KNOWLEDGE", policy.slices.get("KNOWLEDGE", "")),
        "Knowledge source priority:",
        " > ".join(policy.source_priority),
        "Scope guardrail: Keep generated questions and feedback aligned with teacher policy and curriculum context.",
    ]
    return "\n\n".join(block for block in blocks if block.strip())


def _compile_runtime_policy(context: UnifiedContext, capability: str) -> RuntimePolicy:
    teacher_spec = _get_teacher_spec(context)
    slices: dict[str, str] = {}
    sources: dict[str, str] = {}
    for slice_name in SLICE_NAMES:
        value, source = _resolve_slice(slice_name, teacher_spec, context)
        if value:
            slices[slice_name] = value
            sources[slice_name] = source

    knowledge_policy = _resolve_knowledge_policy(teacher_spec, slices)
    return RuntimePolicy(
        capability=capability,
        slices=slices,
        sources=sources,
        knowledge_policy=knowledge_policy,
        source_priority=list(SOURCE_PRIORITY),
    )


def _get_teacher_spec(context: UnifiedContext) -> dict[str, Any]:
    candidates = [
        context.metadata.get("teacher_spec_compiled"),
        context.metadata.get("teacher_spec"),
        context.config_overrides.get("teacher_spec"),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            return candidate
    return {}


def _resolve_slice(
    slice_name: str,
    teacher_spec: dict[str, Any],
    context: UnifiedContext,
) -> tuple[str, str]:
    keys = [slice_name, slice_name.lower()]
    for key in keys:
        value = teacher_spec.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip(), f"teacher_spec.{key}"

    if slice_name == "CURRICULUM":
        raw = context.metadata.get("curriculum_excerpt")
        if isinstance(raw, str) and raw.strip():
            return raw.strip(), "metadata.curriculum_excerpt"

    if slice_name == "RULES":
        raw = context.metadata.get("teacher_rules")
        if isinstance(raw, str) and raw.strip():
            return raw.strip(), "metadata.teacher_rules"

    return "", ""


def _resolve_knowledge_policy(teacher_spec: dict[str, Any], slices: dict[str, str]) -> str:
    raw = teacher_spec.get("knowledge_policy")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    knowledge_slice = slices.get("KNOWLEDGE", "")
    if "kb_preferred" in knowledge_slice.lower():
        return "kb_preferred"
    return DEFAULT_KNOWLEDGE_POLICY


def _slice_block(name: str, content: str) -> str:
    text = content.strip() or "(not provided)"
    return f"[{name}]\n{text}"
