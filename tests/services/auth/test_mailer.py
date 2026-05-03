from __future__ import annotations

from email.message import EmailMessage

from deeptutor.services.auth.mailer import AuthEmailDeliverySettings
from deeptutor.services.auth.mailer import AuthEmailDeliveryConfigError
from deeptutor.services.auth.mailer import build_password_reset_email
from deeptutor.services.auth.mailer import build_verification_email
from deeptutor.services.auth.mailer import deliver_auth_email
from deeptutor.services.auth.mailer import send_auth_email


class _FakeSMTP:
    def __init__(self, host: str, port: int, timeout: int | None = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.started_tls = False
        self.logged_in = None
        self.sent_messages: list[EmailMessage] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def starttls(self, context=None) -> None:
        self.started_tls = True

    def login(self, username: str, password: str) -> None:
        self.logged_in = (username, password)

    def send_message(self, message: EmailMessage) -> None:
        self.sent_messages.append(message)


def test_build_password_reset_email_includes_reset_link() -> None:
    message = build_password_reset_email(
        to_email="teacher@example.com",
        display_name="Teacher One",
        reset_url="https://app.example.com/reset-password?token=abc",
        from_address="noreply@example.com",
        reply_to_address="support@example.com",
        reply_to_name="DeepTutor Support",
    )

    assert message["To"] == "teacher@example.com"
    assert message["Reply-To"] == "DeepTutor Support <support@example.com>"
    assert "Teacher One" in message.get_content()
    assert "reset-password?token=abc" in message.get_content()


def test_build_verification_email_includes_verify_link() -> None:
    message = build_verification_email(
        to_email="student@example.com",
        display_name="Student One",
        verify_url="https://app.example.com/verify-email?token=xyz",
        from_address="noreply@example.com",
    )

    assert message["To"] == "student@example.com"
    assert "Student One" in message.get_content()
    assert "verify-email?token=xyz" in message.get_content()


def test_send_auth_email_uses_configured_smtp_transport(monkeypatch) -> None:
    captured: list[_FakeSMTP] = []

    def _smtp_factory(host: str, port: int, timeout: int | None = None) -> _FakeSMTP:
        smtp = _FakeSMTP(host, port, timeout=timeout)
        captured.append(smtp)
        return smtp

    monkeypatch.setattr("deeptutor.services.auth.mailer.smtplib.SMTP", _smtp_factory)

    settings = AuthEmailDeliverySettings(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_username="mailer-user",
        smtp_password="mailer-pass",
        smtp_use_tls=True,
        from_address="noreply@example.com",
    )
    message = build_password_reset_email(
        to_email="teacher@example.com",
        display_name="Teacher One",
        reset_url="https://app.example.com/reset-password?token=abc",
        from_address="noreply@example.com",
    )

    send_auth_email(settings, message)

    assert len(captured) == 1
    smtp = captured[0]
    assert smtp.host == "smtp.example.com"
    assert smtp.port == 587
    assert smtp.started_tls is True
    assert smtp.logged_in == ("mailer-user", "mailer-pass")
    assert smtp.sent_messages[0]["To"] == "teacher@example.com"


def test_deliver_auth_email_skips_when_transport_is_not_configured() -> None:
    settings = AuthEmailDeliverySettings(delivery_mode="auto")
    message = build_verification_email(
        to_email="student@example.com",
        display_name="Student One",
        verify_url="https://app.example.com/verify-email?token=xyz",
        from_address="noreply@example.com",
    )

    result = deliver_auth_email(settings, message)

    assert result.status == "skipped"
    assert result.detail == "smtp-not-configured"


def test_deliver_auth_email_requires_transport_in_required_mode() -> None:
    settings = AuthEmailDeliverySettings(delivery_mode="required")
    message = build_verification_email(
        to_email="student@example.com",
        display_name="Student One",
        verify_url="https://app.example.com/verify-email?token=xyz",
        from_address="noreply@example.com",
    )

    try:
        deliver_auth_email(settings, message)
    except AuthEmailDeliveryConfigError as exc:
        assert "required" in str(exc).lower()
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected AuthEmailDeliveryConfigError")


def test_delivery_settings_reject_conflicting_tls_and_ssl() -> None:
    try:
        AuthEmailDeliverySettings(
            smtp_host="smtp.example.com",
            from_address="noreply@example.com",
            smtp_use_tls=True,
            smtp_use_ssl=True,
        )
    except ValueError as exc:
        assert "mutually exclusive" in str(exc)
    else:  # pragma: no cover - defensive
        raise AssertionError("Expected ValueError")
