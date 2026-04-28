# PR Note: Baseline Pytest Collection Blocker

## Summary

- add minimal test package markers to prevent duplicate basename collisions during pytest collection
- keep the fix scoped to `tests/` layout stabilization
- document that post-collection baseline failures remain out of scope for this branch

## Mermaid

```mermaid
flowchart LR
  A[tests/agents/math_animator/test_request_config.py] --> P[pytest import namespace]
  B[tests/agents/research/test_request_config.py] --> P
  C[tests/services/llm/test_utils.py] --> P
  D[tests/agents/math_animator/test_utils.py] --> P
  P --> F[Package markers prevent basename collisions]
```

## Main System Map

- Not updated. This fix affects test discovery only.
