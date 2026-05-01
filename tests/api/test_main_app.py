from __future__ import annotations

import logging
from pathlib import Path
from types import SimpleNamespace

import pytest
from starlette.requests import Request
from starlette.responses import Response

from deeptutor.api import main as api_main


def test_suppress_ws_noise_filters_connection_churn() -> None:
    filter_ = api_main._SuppressWsNoise()
    quiet_record = logging.LogRecord(
        name="uvicorn.error",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="WebSocket connection open",
        args=(),
        exc_info=None,
    )
    normal_record = logging.LogRecord(
        name="uvicorn.error",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Request completed",
        args=(),
        exc_info=None,
    )

    assert filter_.filter(quiet_record) is False
    assert filter_.filter(normal_record) is True


def test_rate_limit_helpers_use_policy_prefix() -> None:
    assert api_main._resolve_rate_limit("/api/v1/marketplace/import/demo") == (
        "/api/v1/marketplace/import",
        20,
        60,
    )
    assert api_main._resolve_rate_limit("/api/v1/question/generate") == ("/api/v1/question", 40, 60)
    assert api_main._resolve_rate_limit("/api/v1/other") == ("/api/v1", 120, 60)
    assert (
        api_main._build_rate_limit_bucket_key("127.0.0.1", "/api/v1/question/generate")
        == "127.0.0.1:/api/v1/question"
    )


def test_validate_tool_consistency_accepts_registered_manifests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.runtime.registry.capability_registry.get_capability_registry",
        lambda: SimpleNamespace(get_manifests=lambda: [{"tools_used": ["rag", "reason"]}]),
    )
    monkeypatch.setattr(
        "deeptutor.runtime.registry.tool_registry.get_tool_registry",
        lambda: SimpleNamespace(list_tools=lambda: ["rag", "reason", "brainstorm"]),
    )

    api_main.validate_tool_consistency()


def test_validate_tool_consistency_rejects_drift(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.runtime.registry.capability_registry.get_capability_registry",
        lambda: SimpleNamespace(get_manifests=lambda: [{"tools_used": ["rag", "missing_tool"]}]),
    )
    monkeypatch.setattr(
        "deeptutor.runtime.registry.tool_registry.get_tool_registry",
        lambda: SimpleNamespace(list_tools=lambda: ["rag"]),
    )

    with pytest.raises(RuntimeError) as excinfo:
        api_main.validate_tool_consistency()

    assert "missing_tool" in str(excinfo.value)


def test_validate_tool_consistency_reraises_loader_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "deeptutor.runtime.registry.capability_registry.get_capability_registry",
        lambda: (_ for _ in ()).throw(ValueError("registry boom")),
    )

    with pytest.raises(ValueError) as excinfo:
        api_main.validate_tool_consistency()

    assert "registry boom" in str(excinfo.value)


@pytest.mark.asyncio
async def test_safe_output_static_files_blocks_non_public_path(tmp_path: Path) -> None:
    static_dir = tmp_path / "public"
    static_dir.mkdir()
    (static_dir / "allowed.txt").write_text("ok")

    static_files = api_main.SafeOutputStaticFiles(
        directory=str(static_dir),
        path_service=SimpleNamespace(is_public_output_path=lambda path: path == "allowed.txt"),
    )

    denied_scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/outputs/private.txt",
        "headers": [],
    }
    allowed_scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/outputs/allowed.txt",
        "headers": [],
    }

    with pytest.raises(api_main.HTTPException) as excinfo:
        await static_files.get_response("private.txt", denied_scope)
    allowed_response = await static_files.get_response("allowed.txt", allowed_scope)

    assert excinfo.value.status_code == 404
    assert allowed_response.status_code == 200


def _build_request(path: str, *, client_host: str = "127.0.0.1") -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": path,
            "headers": [],
            "client": (client_host, 12345),
            "scheme": "http",
            "server": ("testserver", 80),
        }
    )


@pytest.mark.asyncio
async def test_api_rate_limit_skips_non_api_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    request = _build_request("/healthz")
    called = False

    async def call_next(_request: Request) -> Response:
        nonlocal called
        called = True
        return Response(status_code=204)

    response = await api_main.api_rate_limit(request, call_next)

    assert response.status_code == 204
    assert called is True


@pytest.mark.asyncio
async def test_api_rate_limit_enforces_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    api_main._rate_limit_store.clear()
    request = _build_request("/api/v1/question/generate")
    call_count = 0
    now_values = iter([100.0] * 41 + [101.0])

    monkeypatch.setattr(api_main, "monotonic", lambda: next(now_values))

    async def call_next(_request: Request) -> Response:
        nonlocal call_count
        call_count += 1
        return Response(status_code=200)

    for _ in range(40):
        response = await api_main.api_rate_limit(request, call_next)
        assert response.status_code == 200

    limited = await api_main.api_rate_limit(request, call_next)

    assert call_count == 40
    assert limited.status_code == 429
    assert limited.headers["Retry-After"] == "60"
    assert limited.body == b'{"detail":"Too Many Requests"}'


@pytest.mark.asyncio
async def test_api_rate_limit_evicts_expired_events(monkeypatch: pytest.MonkeyPatch) -> None:
    api_main._rate_limit_store.clear()
    request = _build_request("/api/v1/solve/demo")
    key = api_main._build_rate_limit_bucket_key("127.0.0.1", "/api/v1/solve/demo")
    api_main._rate_limit_store[key].extend([1.0, 2.0])

    monkeypatch.setattr(api_main, "monotonic", lambda: 100.0)

    async def call_next(_request: Request) -> Response:
        return Response(status_code=202)

    response = await api_main.api_rate_limit(request, call_next)

    assert response.status_code == 202
    assert list(api_main._rate_limit_store[key]) == [100.0]


@pytest.mark.asyncio
async def test_selective_access_log_only_logs_non_200(monkeypatch: pytest.MonkeyPatch) -> None:
    request = _build_request("/api/v1/demo", client_host="10.0.0.5")
    messages: list[tuple] = []
    monkeypatch.setattr(api_main, "_access_logger", SimpleNamespace(info=lambda *args: messages.append(args)))

    async def ok_call_next(_request: Request) -> Response:
        return Response(status_code=200)

    async def error_call_next(_request: Request) -> Response:
        return Response(status_code=503)

    ok_response = await api_main.selective_access_log(request, ok_call_next)
    error_response = await api_main.selective_access_log(
        request,
        error_call_next,
    )

    assert ok_response.status_code == 200
    assert error_response.status_code == 503
    assert len(messages) == 1
    assert messages[0][0] == '%s - "%s %s" %d'
    assert messages[0][1:] == ("10.0.0.5", "GET", "/api/v1/demo", 503)


@pytest.mark.asyncio
async def test_lifespan_starts_and_stops_services(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    event_bus = SimpleNamespace(
        start=lambda: calls.append("event_bus.start") or asyncio.sleep(0),
        stop=lambda: calls.append("event_bus.stop") or asyncio.sleep(0),
    )
    tutorbot_manager = SimpleNamespace(
        auto_start_bots=lambda: calls.append("tutorbot.start") or asyncio.sleep(0),
        stop_all=lambda: calls.append("tutorbot.stop") or asyncio.sleep(0),
    )

    monkeypatch.setattr(api_main, "validate_tool_consistency", lambda: calls.append("validate"))
    monkeypatch.setattr(
        "deeptutor.services.llm.get_llm_client",
        lambda: SimpleNamespace(config=SimpleNamespace(model="gpt-test")),
    )
    monkeypatch.setattr("deeptutor.events.event_bus.get_event_bus", lambda: event_bus)
    monkeypatch.setattr("deeptutor.services.tutorbot.get_tutorbot_manager", lambda: tutorbot_manager)

    async with api_main.lifespan(api_main.app):
        calls.append("inside")

    assert calls == [
        "validate",
        "event_bus.start",
        "tutorbot.start",
        "inside",
        "tutorbot.stop",
        "event_bus.stop",
    ]


@pytest.mark.asyncio
async def test_lifespan_tolerates_startup_and_shutdown_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    warnings: list[str] = []
    monkeypatch.setattr(api_main, "validate_tool_consistency", lambda: None)
    monkeypatch.setattr(
        api_main.logger,
        "warning",
        lambda message: warnings.append(message),
    )
    monkeypatch.setattr(
        "deeptutor.services.llm.get_llm_client",
        lambda: (_ for _ in ()).throw(RuntimeError("llm down")),
    )
    monkeypatch.setattr(
        "deeptutor.events.event_bus.get_event_bus",
        lambda: SimpleNamespace(
            start=lambda: (_ for _ in ()).throw(RuntimeError("bus down")),
            stop=lambda: (_ for _ in ()).throw(RuntimeError("bus stop down")),
        ),
    )
    monkeypatch.setattr(
        "deeptutor.services.tutorbot.get_tutorbot_manager",
        lambda: SimpleNamespace(
            auto_start_bots=lambda: (_ for _ in ()).throw(RuntimeError("bots down")),
            stop_all=lambda: (_ for _ in ()).throw(RuntimeError("bots stop down")),
        ),
    )

    async with api_main.lifespan(api_main.app):
        pass

    assert any("Failed to initialize LLM client" in item for item in warnings)
    assert any("Failed to start EventBus" in item for item in warnings)
    assert any("Failed to auto-start TutorBots" in item for item in warnings)
    assert any("Failed to stop TutorBots" in item for item in warnings)
    assert any("Failed to stop EventBus" in item for item in warnings)
