from __future__ import annotations

import json
from pathlib import Path

from deeptutor.services.evidence.diagnosis import build_student_diagnosis


def _load_casepack() -> dict:
    root = Path(__file__).resolve().parents[3]
    path = root / "ai_first" / "evidence" / "casepacks" / "diagnosis-validation-pack.json"
    return json.loads(path.read_text())


def test_validation_casepack_has_expected_shape_and_traceability() -> None:
    payload = _load_casepack()

    assert payload["pack_id"] == "diagnosis-validation-pack"
    assert payload["version"] == 1
    assert payload["policy"] == "rule_assisted_teacher_review"
    assert len(payload["cases"]) >= 5

    for case in payload["cases"]:
        assert case["case_id"]
        assert case["title"]
        assert case["validation_objective"]
        assert isinstance(case["observations"], list)
        assert case["expected"]["mode"] in {"diagnosis", "abstain"}
        assert case["source_refs"]


def test_validation_casepack_cases_match_current_diagnosis_behavior() -> None:
    payload = _load_casepack()

    for case in payload["cases"]:
        result = build_student_diagnosis(
            student_id=case["student_id"],
            observations=case["observations"],
            student_state=case.get("student_state"),
        )
        expected = case["expected"]

        if expected["mode"] == "diagnosis":
            assert result["observed"]["abstained"] is False
            assert result["inferred"][0]["diagnosis_type"] == expected["diagnosis_type"]
            assert result["recommended_actions"][0]["action_type"] == expected["action_type"]
            if "confidence_tags" in expected:
                assert result["inferred"][0]["confidence_tag"] in expected["confidence_tags"]
        else:
            assert result["observed"]["abstained"] is True
            assert result["observed"]["abstain_reason_code"] == expected["abstain_reason_code"]
            assert result["inferred"] == []
            assert result["recommended_actions"] == []

