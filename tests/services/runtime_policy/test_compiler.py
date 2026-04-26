from __future__ import annotations

from deeptutor.services.agent_spec.service import AgentSpecService
from deeptutor.core.context import UnifiedContext
from deeptutor.services.runtime_policy import SOURCE_PRIORITY, ensure_runtime_policy
from deeptutor.services.runtime_policy import compiler as runtime_policy_compiler


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


def test_runtime_policy_resolves_agent_spec_pack(monkeypatch, tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            "identity": {
                "agent_name": "Fraction Coach",
                "subject": "Mathematics",
                "grade_band": "Grade 6",
                "tone": "Warm and direct",
                "primary_language": "Vietnamese",
                "persona_summary": "A teacher-defined tutor for fraction practice.",
            },
            "soul": {
                "teaching_philosophy": "Use evidence before intervention.",
                "when_student_wrong": "Diagnose the misconception.",
                "when_student_stuck": "Offer one scaffold at a time.",
                "encouragement_style": "Calm and specific.",
            },
            "rules": {
                "do_not_solve_directly": "yes",
                "max_session_minutes": "25",
                "hint_policy": "One hint at a time.",
                "escalation_rule": "Escalate after repeated confusion.",
                "guardrails": "Never finish the answer for the student.",
            },
        },
        files={
            "ASSESSMENT.md": "# Assessment\n\n## Evidence Signals\n\n- Ask one concept per question.\n",
            "WORKFLOW.md": "# Workflow\n\n## Session Flow\n\n1. Teach\n2. Practice\n3. Check\n",
            "KNOWLEDGE.md": "# Knowledge\n\n## Retrieval Policy\n\n- Prefer teacher-authored materials first.\n- Use kb_preferred retrieval.\n",
        },
    )
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    context = UnifiedContext(metadata={"agent_spec_id": "fraction-coach"})
    policy = ensure_runtime_policy(context, "chat")
    payload = policy.to_dict()

    assert payload["agent_spec_id"] == "fraction-coach"
    assert payload["slices"]["IDENTITY"].startswith("# Identity")
    assert payload["slices"]["SOUL"].startswith("# Soul")
    assert payload["slices"]["WORKFLOW"].startswith("# Workflow")
    assert payload["debug"]["agent_spec_id"] == "fraction-coach"


def test_runtime_policy_reads_teacher_kb_context_from_metadata(monkeypatch) -> None:
    class FakeKBManager:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def get_info(self, _name: str) -> dict:
            return {
                "metadata": {
                    "subject": "Mathematics",
                    "grade": "10",
                    "curriculum": "Vietnam National Curriculum",
                    "learning_objectives": ["Quadratic equations", "Graph reading"],
                }
            }

    monkeypatch.setattr(runtime_policy_compiler, "KnowledgeBaseManager", FakeKBManager)

    context = UnifiedContext(knowledge_bases=["algebra-pack"])
    policy = ensure_runtime_policy(context, "deep_question")
    payload = policy.to_dict()

    assert "Knowledge Pack: algebra-pack" in payload["teacher_kb_context"]
    assert payload["sources"]["KNOWLEDGE_BASE"] == "knowledge_base.algebra-pack.metadata"
    assert payload["slices"]["CURRICULUM"].startswith("Knowledge Pack: algebra-pack")


def test_runtime_policy_prefers_pinned_agent_spec_version(monkeypatch, tmp_path) -> None:
    service = AgentSpecService(tmp_path / "agent_specs")
    service.create_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            "identity": {"agent_name": "Fraction Coach"},
            "soul": {"teaching_philosophy": "Version one philosophy."},
            "rules": {"guardrails": "Version one guardrails."},
        },
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion one.\n"},
    )
    service.save_pack(
        agent_id="fraction-coach",
        display_name="Fraction Coach",
        structured={
            "identity": {"agent_name": "Fraction Coach"},
            "soul": {"teaching_philosophy": "Version two philosophy."},
            "rules": {"guardrails": "Version two guardrails."},
        },
        files={"WORKFLOW.md": "# Workflow\n\n## Session Flow\n\nVersion two.\n"},
    )
    monkeypatch.setattr(runtime_policy_compiler, "get_agent_spec_service", lambda: service)

    context = UnifiedContext(
        metadata={
            "agent_spec_id": "fraction-coach",
            "session_preferences": {
                "agent_spec_pin": {
                    "agent_spec_id": "fraction-coach",
                    "version": 1,
                    "updated_at": "2026-04-27T00:00:00Z",
                }
            },
        }
    )
    policy = ensure_runtime_policy(context, "chat")
    payload = policy.to_dict()

    assert payload["agent_spec_id"] == "fraction-coach"
    assert payload["agent_spec_version"] == 1
    assert "Version one philosophy." in payload["slices"]["SOUL"]
    assert "Version two philosophy." not in payload["slices"]["SOUL"]
    assert payload["debug"]["agent_spec_version"] == 1
