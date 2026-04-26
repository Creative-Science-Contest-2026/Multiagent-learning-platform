"""Runtime policy assembly for teacher-spec driven capabilities."""

from .compiler import (
    SOURCE_PRIORITY,
    RuntimePolicy,
    ensure_runtime_policy,
    format_assessment_context,
    format_chat_system_context,
)

__all__ = [
    "SOURCE_PRIORITY",
    "RuntimePolicy",
    "ensure_runtime_policy",
    "format_assessment_context",
    "format_chat_system_context",
]
