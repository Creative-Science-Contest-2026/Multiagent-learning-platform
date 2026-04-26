from __future__ import annotations

from deeptutor.core.context import UnifiedContext
from deeptutor.services.runtime_policy import SOURCE_PRIORITY, ensure_runtime_policy


def test_runtime_policy_compiles_teacher_slices_and_priority() -> None:
    context = UnifiedContext(
        metadata={
            "teacher_spec": {
                "SOUL": "Be calm and encouraging.",
                "RULES": "Stay inside algebra scope.",
                "WORKFLOW": "Explain then practice then check.",
                "ASSESSMENT": "Ask one concept per question.",
                "KNOWLEDGE": "Use kb_preferred when possible.",
            },
            "curriculum_excerpt": "Linear equations and inequalities.",
        }
    )

    policy = ensure_runtime_policy(context, "chat")
    payload = policy.to_dict()

    assert payload["slices"]["SOUL"] == "Be calm and encouraging."
    assert payload["slices"]["CURRICULUM"] == "Linear equations and inequalities."
    assert payload["knowledge_policy"] == "kb_preferred"
    assert payload["source_priority"] == SOURCE_PRIORITY
    assert "SOUL" in payload["debug"]["applied_slices"]
    assert "MARKETPLACE" not in payload["debug"]["applied_slices"]


def test_runtime_policy_uses_metadata_fallback_for_rules() -> None:
    context = UnifiedContext(metadata={"teacher_rules": "Always request justification."})

    policy = ensure_runtime_policy(context, "deep_question")
    payload = policy.to_dict()

    assert payload["slices"]["RULES"] == "Always request justification."
    assert payload["sources"]["RULES"] == "metadata.teacher_rules"
    assert payload["knowledge_policy"] == "kb_preferred"
