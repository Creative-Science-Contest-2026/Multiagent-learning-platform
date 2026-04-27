import json
from pathlib import Path


def test_casepack_has_required_top_level_shape():
    payload = json.loads(Path("ai_first/evidence/casepack.json").read_text())
    assert payload["version"]
    assert isinstance(payload["categories"], list)
    assert isinstance(payload["cases"], list)
    assert payload["cases"]


def test_every_case_has_required_fields_and_known_category():
    payload = json.loads(Path("ai_first/evidence/casepack.json").read_text())
    allowed = set(payload["categories"])
    required = {
        "id",
        "category",
        "title",
        "objective",
        "product_surface",
        "observed",
        "inferred",
        "recommended_action",
        "teacher_review_framing",
        "unsafe_overclaim",
        "expected_artifacts",
    }
    for case in payload["cases"]:
        assert required.issubset(case.keys())
        assert case["category"] in allowed
        assert case["expected_artifacts"]
