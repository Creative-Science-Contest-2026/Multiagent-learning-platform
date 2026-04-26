"""Prompt manager path resolution tests."""

from __future__ import annotations

from deeptutor.services.prompt import get_prompt_manager


def test_prompt_manager_loads_prompts_from_deeptutor_tree() -> None:
    manager = get_prompt_manager()
    manager.clear_cache()

    prompts = manager.load_prompts(
        module_name="question",
        agent_name="idea_agent",
        language="en",
    )

    assert "generate_ideas" in prompts


def test_prompt_manager_builds_runtime_policy_prompt_with_explicit_sections() -> None:
    manager = get_prompt_manager()

    prompt = manager.build_runtime_policy_prompt(
        title="Teacher Runtime Policy:",
        sections=[
            ("IDENTITY", "Math tutor for grade 6."),
            ("SOUL", "Stay calm and encouraging."),
            ("RULES", ""),
        ],
        source_priority=["teacher_kb", "curriculum_excerpt", "teacher_rules"],
        guardrail="Stay within teacher-defined scope.",
        extra_blocks=["Teacher Spec Reference:\nfraction-coach"],
    )

    assert "Teacher Runtime Policy:" in prompt
    assert "[IDENTITY]\nMath tutor for grade 6." in prompt
    assert "[SOUL]\nStay calm and encouraging." in prompt
    assert "[RULES]" not in prompt
    assert "teacher_kb > curriculum_excerpt > teacher_rules" in prompt
    assert "Teacher Spec Reference:\nfraction-coach" in prompt
    assert "Scope guardrail: Stay within teacher-defined scope." in prompt
