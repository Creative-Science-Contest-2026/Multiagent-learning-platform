from deeptutor.api import main


def test_rate_limit_bucket_key_uses_matched_policy_prefix() -> None:
    import_key = main._build_rate_limit_bucket_key(
        client_ip="127.0.0.1",
        path="/api/v1/marketplace/import/shared-pack",
    )
    list_key = main._build_rate_limit_bucket_key(
        client_ip="127.0.0.1",
        path="/api/v1/marketplace/list",
    )

    assert import_key != list_key
    assert import_key.endswith("/api/v1/marketplace/import")
    assert list_key.endswith("/api/v1")


def test_rate_limit_bucket_key_is_stable_within_a_policy_prefix() -> None:
    first = main._build_rate_limit_bucket_key(
        client_ip="127.0.0.1",
        path="/api/v1/question",
    )
    second = main._build_rate_limit_bucket_key(
        client_ip="127.0.0.1",
        path="/api/v1/question/stream",
    )

    assert first == second
