#!/usr/bin/env bash

set -euo pipefail

if [[ -n "${PYTHON_BIN:-}" ]]; then
  python_bin="$PYTHON_BIN"
elif [[ -x ".venv/bin/python" ]]; then
  python_bin=".venv/bin/python"
else
  python_bin="python"
fi

"$python_bin" -m pytest \
  tests/api/test_main_app.py \
  tests/api/test_agent_specs_router.py \
  tests/api/test_assessment_router.py \
  tests/api/test_dashboard_router.py \
  tests/api/test_knowledge_router.py \
  tests/api/test_marketplace_router.py \
  tests/api/test_question_router.py \
  tests/api/test_unified_ws_turn_runtime.py \
  tests/knowledge/test_kb_metadata_normalization.py \
  tests/knowledge/test_progress_tracker.py \
  tests/services/agent_spec/test_service.py \
  tests/services/evidence/test_intervention_effectiveness.py \
  tests/services/runtime_policy/test_compiler.py \
  tests/services/session \
  --cov=deeptutor.api.main \
  --cov=deeptutor.api.routers.agent_specs \
  --cov=deeptutor.api.routers.assessment \
  --cov=deeptutor.api.routers.dashboard \
  --cov=deeptutor.api.routers.marketplace \
  --cov=deeptutor.api.routers.knowledge \
  --cov=deeptutor.api.routers.question \
  --cov=deeptutor.api.routers.unified_ws \
  --cov=deeptutor.services.agent_spec.service \
  --cov=deeptutor.services.assessment.analysis \
  --cov=deeptutor.services.assessment.recommendation_engine \
  --cov=deeptutor.services.evidence.diagnosis \
  --cov=deeptutor.services.evidence.diagnosis_feedback \
  --cov=deeptutor.services.evidence.diagnosis_taxonomy \
  --cov=deeptutor.services.evidence.evidence_sufficiency \
  --cov=deeptutor.services.evidence.extractor \
  --cov=deeptutor.services.evidence.intervention_assignments \
  --cov=deeptutor.services.evidence.intervention_effectiveness \
  --cov=deeptutor.services.evidence.recommendation_acks \
  --cov=deeptutor.services.evidence.recommendation_feedback \
  --cov=deeptutor.services.evidence.teacher_actions \
  --cov=deeptutor.services.evidence.teacher_insights \
  --cov=deeptutor.services.evidence.teacher_overrides \
  --cov=deeptutor.services.runtime_policy.compiler \
  --cov=deeptutor.services.session.sqlite_store \
  --cov=deeptutor.services.session.turn_runtime \
  --cov-report=term \
  --cov-report=json:coverage-focus.json \
  --cov-fail-under=80 \
  -q

"$python_bin" -m compileall deeptutor
