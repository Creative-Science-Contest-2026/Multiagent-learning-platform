"""Compile teacher-authored spec slices into a runtime policy contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from deeptutor.core.context import UnifiedContext
from deeptutor.knowledge.manager import KnowledgeBaseManager
from deeptutor.services.agent_spec import get_agent_spec_service
from deeptutor.services.path_service import get_path_service
from deeptutor.services.prompt import get_prompt_manager

SLICE_NAMES = ["IDENTITY", "SOUL", "RULES", "WORKFLOW", "ASSESSMENT", "KNOWLEDGE", "CURRICULUM"]
SOURCE_PRIORITY = [
    "teacher_kb",
    "curriculum_excerpt",
    "teacher_rules",
    "llm_prior_knowledge",
]
DEFAULT_KNOWLEDGE_POLICY = "kb_preferred"
SPEC_FILE_TO_SLICE = {
    "IDENTITY.md": "IDENTITY",
    "SOUL.md": "SOUL",
    "CURRICULUM.md": "CURRICULUM",
    "RULES.md": "RULES",
    "ASSESSMENT.md": "ASSESSMENT",
    "WORKFLOW.md": "WORKFLOW",
    "KNOWLEDGE.md": "KNOWLEDGE",
}


@dataclass
class RuntimePolicy:
    """Serializable policy object injected into runtime context."""

    capability: str
    agent_spec_id: str
    agent_spec_version: int | None
    slices: dict[str, str]
    sources: dict[str, str]
    knowledge_policy: str
    source_priority: list[str]
    teacher_kb_context: str = ""
    student_state: dict[str, Any] | None = None
    session_state: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        applied = [name for name, value in self.slices.items() if value.strip()]
        missing = [name for name in SLICE_NAMES if name not in applied]
        return {
            "capability": self.capability,
            "agent_spec_id": self.agent_spec_id,
            "agent_spec_version": self.agent_spec_version,
            "slices": dict(self.slices),
            "sources": dict(self.sources),
            "knowledge_policy": self.knowledge_policy,
            "source_priority": list(self.source_priority),
            "teacher_kb_context": self.teacher_kb_context,
            "student_state": dict(self.student_state or {}),
            "session_state": dict(self.session_state or {}),
            "debug": {
                "applied_slices": applied,
                "missing_slices": missing,
                "slice_sources": dict(self.sources),
                "agent_spec_id": self.agent_spec_id,
                "agent_spec_version": self.agent_spec_version,
                "has_teacher_kb_context": bool(self.teacher_kb_context.strip()),
            },
        }


def ensure_runtime_policy(context: UnifiedContext, capability: str) -> RuntimePolicy:
    """Return existing compiled policy from context metadata or compile one."""
    existing = context.metadata.get("runtime_policy")
    if isinstance(existing, dict):
        return RuntimePolicy(
            capability=str(existing.get("capability") or capability),
            agent_spec_id=str(existing.get("agent_spec_id") or ""),
            agent_spec_version=(
                int(existing["agent_spec_version"])
                if existing.get("agent_spec_version") is not None
                else None
            ),
            slices={k: str(v or "") for k, v in dict(existing.get("slices") or {}).items()},
            sources={k: str(v or "") for k, v in dict(existing.get("sources") or {}).items()},
            knowledge_policy=str(existing.get("knowledge_policy") or DEFAULT_KNOWLEDGE_POLICY),
            source_priority=list(existing.get("source_priority") or SOURCE_PRIORITY),
            teacher_kb_context=str(existing.get("teacher_kb_context") or ""),
            student_state=dict(existing.get("student_state") or {}),
            session_state=dict(existing.get("session_state") or {}),
        )

    policy = _compile_runtime_policy(context=context, capability=capability)
    context.metadata.setdefault("teacher_spec_compiled", _export_teacher_spec(policy))
    context.metadata["runtime_policy"] = policy.to_dict()
    return policy


def build_runtime_policy_audit(
    *,
    agent_spec_id: str,
    capability: str = "chat",
    version: int | None = None,
    knowledge_bases: list[str] | None = None,
) -> dict[str, Any]:
    """Build a serializable runtime-policy audit payload for a selected Agent Spec."""
    service = get_agent_spec_service()
    pack = service.get_pack_version(agent_spec_id, int(version)) if version is not None else service.get_pack(agent_spec_id)
    metadata: dict[str, Any] = {
        "agent_spec_id": str(pack.get("agent_id") or agent_spec_id),
        "teacher_spec_compiled": _pack_to_teacher_spec(pack),
    }
    context = UnifiedContext(
        active_capability=capability,
        knowledge_bases=list(knowledge_bases or []),
        config_overrides={"agent_spec_id": str(pack.get("agent_id") or agent_spec_id)},
        metadata=metadata,
    )
    policy = ensure_runtime_policy(context, capability)
    return {
        "agent_spec_id": policy.agent_spec_id,
        "agent_spec_version": policy.agent_spec_version,
        "capability": capability,
        "runtime_policy": policy.to_dict(),
    }


def format_chat_system_context(policy: RuntimePolicy) -> str:
    """Build tutoring-oriented system guidance from assembled slices."""
    sections = [
        ("KNOWLEDGE BASE", policy.teacher_kb_context),
        ("IDENTITY", policy.slices.get("IDENTITY", "")),
        ("SOUL", policy.slices.get("SOUL", "")),
        ("RULES", policy.slices.get("RULES", "")),
        ("WORKFLOW", policy.slices.get("WORKFLOW", "")),
        ("KNOWLEDGE", policy.slices.get("KNOWLEDGE", "")),
        ("CURRICULUM", policy.slices.get("CURRICULUM", "")),
    ]
    if not _has_runtime_guidance(policy, sections):
        return ""
    manager = get_prompt_manager()
    return manager.build_runtime_policy_prompt(
        title="Teacher Runtime Policy:",
        sections=sections,
        source_priority=policy.source_priority,
        extra_blocks=_boundary_blocks(policy),
        guardrail="Stay within teacher-defined scope and clarify uncertainty when evidence is missing.",
    )


def format_assessment_context(policy: RuntimePolicy) -> str:
    """Build assessment-oriented guidance from assembled slices."""
    sections = [
        ("KNOWLEDGE BASE", policy.teacher_kb_context),
        ("IDENTITY", policy.slices.get("IDENTITY", "")),
        ("ASSESSMENT", policy.slices.get("ASSESSMENT", "")),
        ("RULES", policy.slices.get("RULES", "")),
        ("WORKFLOW", policy.slices.get("WORKFLOW", "")),
        ("KNOWLEDGE", policy.slices.get("KNOWLEDGE", "")),
        ("CURRICULUM", policy.slices.get("CURRICULUM", "")),
    ]
    if not _has_runtime_guidance(policy, sections):
        return ""
    manager = get_prompt_manager()
    return manager.build_runtime_policy_prompt(
        title="Teacher Assessment Runtime Policy:",
        sections=sections,
        source_priority=policy.source_priority,
        extra_blocks=_boundary_blocks(policy),
        guardrail="Keep generated questions and feedback aligned with teacher policy and curriculum context.",
    )


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
    agent_spec_id = str(teacher_spec.get("agent_spec_id") or "")
    agent_spec_version = (
        int(teacher_spec["agent_spec_version"])
        if teacher_spec.get("agent_spec_version") is not None
        else None
    )
    teacher_kb_context, teacher_kb_source = _build_teacher_kb_context(context)
    if teacher_kb_source:
        sources.setdefault("KNOWLEDGE_BASE", teacher_kb_source)
    return RuntimePolicy(
        capability=capability,
        agent_spec_id=agent_spec_id,
        agent_spec_version=agent_spec_version,
        slices=slices,
        sources=sources,
        knowledge_policy=knowledge_policy,
        source_priority=list(SOURCE_PRIORITY),
        teacher_kb_context=teacher_kb_context,
        student_state=_extract_mapping(context, "student_state"),
        session_state=_extract_mapping(context, "session_state"),
    )


def _get_teacher_spec(context: UnifiedContext) -> dict[str, Any]:
    candidates = [
        context.metadata.get("teacher_spec_compiled"),
        context.metadata.get("teacher_spec"),
        context.config_overrides.get("teacher_spec"),
        context.metadata.get("agent_spec_compiled"),
        context.config_overrides.get("agent_spec_compiled"),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            normalized = _normalize_teacher_spec(candidate)
            if normalized:
                return normalized

    pin = _resolve_agent_spec_pin(context)
    if pin:
        pinned_agent_id = str(pin.get("agent_spec_id") or "").strip()
        pinned_version = pin.get("version")
        if pinned_agent_id and pinned_version is not None:
            try:
                pack = get_agent_spec_service().get_pack_version(
                    pinned_agent_id,
                    int(pinned_version),
                )
            except FileNotFoundError:
                return {}
            return _normalize_teacher_spec(_pack_to_teacher_spec(pack))

    agent_spec_id = _resolve_agent_spec_id(context)
    if agent_spec_id:
        try:
            pack = get_agent_spec_service().get_pack(agent_spec_id)
        except FileNotFoundError:
            return {}
        return _normalize_teacher_spec(_pack_to_teacher_spec(pack))
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
        kb_excerpt, source = _build_curriculum_excerpt_from_kb(context)
        if kb_excerpt:
            return kb_excerpt, source

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


def _resolve_agent_spec_id(context: UnifiedContext) -> str:
    candidates = [
        context.metadata.get("agent_spec_id"),
        context.config_overrides.get("agent_spec_id"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return ""


def _resolve_agent_spec_pin(context: UnifiedContext) -> dict[str, Any] | None:
    candidates = [
        context.metadata.get("agent_spec_pin"),
        (context.metadata.get("session_preferences") or {}).get("agent_spec_pin")
        if isinstance(context.metadata.get("session_preferences"), dict)
        else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            return candidate
    return None


def _pack_to_teacher_spec(pack: dict[str, Any]) -> dict[str, Any]:
    files = dict(pack.get("files") or {})
    compiled: dict[str, Any] = {
        "agent_spec_id": str(pack.get("agent_id") or ""),
        "agent_spec_version": pack.get("version"),
        "knowledge_policy": str((pack.get("summary") or {}).get("knowledge_policy") or ""),
    }
    for filename, slice_name in SPEC_FILE_TO_SLICE.items():
        value = files.get(filename)
        if isinstance(value, str) and value.strip():
            compiled[slice_name] = value.strip()

    summary = pack.get("summary") or {}
    if isinstance(summary, dict) and isinstance(summary.get("teaching_philosophy"), str):
        compiled.setdefault("SOUL", str(compiled.get("SOUL") or summary.get("teaching_philosophy") or ""))
    return compiled


def _normalize_teacher_spec(candidate: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in candidate.items():
        if isinstance(value, str):
            if value.strip():
                normalized[str(key)] = value.strip()
        elif isinstance(value, dict):
            continue
        elif value is not None:
            normalized[str(key)] = value
    return normalized


def _build_teacher_kb_context(context: UnifiedContext) -> tuple[str, str]:
    kb_name = context.knowledge_bases[0] if context.knowledge_bases else ""
    if not kb_name:
        return "", ""
    try:
        manager = KnowledgeBaseManager(base_dir=str(get_path_service().project_root / "data" / "knowledge_bases"))
        info = manager.get_info(kb_name)
    except Exception:
        return "", ""

    metadata = info.get("metadata") or {}
    if not isinstance(metadata, dict):
        return "", ""

    lines = [f"Knowledge Pack: {kb_name}"]
    for label, key in (
        ("Subject", "subject"),
        ("Grade", "grade"),
        ("Curriculum", "curriculum"),
        ("Language", "language"),
    ):
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            lines.append(f"{label}: {value.strip()}")

    objectives = metadata.get("learning_objectives")
    if isinstance(objectives, list) and objectives:
        objective_lines = [str(item).strip() for item in objectives if str(item).strip()]
        if objective_lines:
            lines.append("Learning objectives:")
            lines.extend(f"- {item}" for item in objective_lines)

    if len(lines) == 1:
        return "", ""
    return "\n".join(lines), f"knowledge_base.{kb_name}.metadata"


def _build_curriculum_excerpt_from_kb(context: UnifiedContext) -> tuple[str, str]:
    teacher_kb_context, source = _build_teacher_kb_context(context)
    return teacher_kb_context, source


def _extract_mapping(context: UnifiedContext, key: str) -> dict[str, Any]:
    for candidate in (context.metadata.get(key), context.config_overrides.get(key)):
        if isinstance(candidate, dict):
            return dict(candidate)
    return {}


def _boundary_blocks(policy: RuntimePolicy) -> list[str]:
    blocks: list[str] = []
    if policy.agent_spec_id:
        blocks.append(f"Teacher Spec Reference:\n{policy.agent_spec_id}")
    if policy.student_state:
        blocks.append("Student State Available:\nUse the provided student state as dynamic context, not immutable policy.")
    if policy.session_state:
        blocks.append("Session State Available:\nUse the provided session state for current-turn context only.")
    return blocks


def _export_teacher_spec(policy: RuntimePolicy) -> dict[str, Any]:
    payload = {
        "agent_spec_id": policy.agent_spec_id,
        "knowledge_policy": policy.knowledge_policy,
    }
    payload.update(policy.slices)
    return payload


def _has_runtime_guidance(policy: RuntimePolicy, sections: list[tuple[str, str]]) -> bool:
    if any(content.strip() for _, content in sections):
        return True
    if policy.agent_spec_id:
        return True
    if policy.student_state or policy.session_state:
        return True
    return False
