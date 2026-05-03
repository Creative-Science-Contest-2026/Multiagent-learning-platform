from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from deeptutor.services.auth.models import AuthSession
from deeptutor.services.auth.models import EmailVerificationToken
from deeptutor.services.auth.models import PasswordResetToken
from deeptutor.services.auth.models import User
from deeptutor.services.auth.models import UserOAuthIdentity
from deeptutor.services.auth.models import UserPasswordCredential
from deeptutor.services.auth.passwords import hash_password
from deeptutor.services.auth.passwords import verify_password
from deeptutor.services.auth.session_tokens import hash_session_secret
from deeptutor.services.auth.session_tokens import mint_session_secret
from deeptutor.services.db import get_auth_session_factory
from deeptutor.services.db import init_auth_schema


class AuthService:
    def __init__(self, session_factory=None) -> None:
        self._session_factory = session_factory or get_auth_session_factory()
        init_auth_schema()

    def _session(self) -> Session:
        return self._session_factory()

    @staticmethod
    def _serialize_user(user: User) -> dict[str, str | None]:
        return {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "role": str(user.role.value if hasattr(user.role, "value") else user.role),
            "email_verified_at": user.email_verified_at.isoformat() if user.email_verified_at else None,
        }

    def create_user(self, *, email: str, display_name: str, role: str, password: str) -> dict[str, str]:
        normalized_email = email.strip().lower()
        with self._session() as session:
            existing = session.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
            if existing is not None:
                raise ValueError("email_exists")

            user = User(
                email=normalized_email,
                display_name=display_name.strip(),
                role=role,
                status="active",
            )
            session.add(user)
            session.flush()
            session.add(
                UserPasswordCredential(
                    user_id=user.id,
                    password_hash=hash_password(password),
                )
            )
            session.commit()
            return self._serialize_user(user)

    def authenticate_user(self, *, email: str, password: str) -> dict[str, str] | None:
        normalized_email = email.strip().lower()
        with self._session() as session:
            user = session.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
            if user is None:
                return None
            credential = session.get(UserPasswordCredential, user.id)
            if credential is None or not verify_password(password, credential.password_hash):
                return None
            return self._serialize_user(user)

    def create_auth_session(
        self,
        *,
        user_id: str,
        user_agent: str | None,
        ip_address: str | None,
    ) -> tuple[str, dict[str, str | None]]:
        secret = mint_session_secret()
        expires_at = datetime.utcnow() + timedelta(days=14)
        with self._session() as session:
            auth_session = AuthSession(
                user_id=user_id,
                session_secret_hash=hash_session_secret(secret),
                user_agent=user_agent,
                ip_address=ip_address,
                expires_at=expires_at,
                last_seen_at=datetime.utcnow(),
            )
            session.add(auth_session)
            session.commit()
            return secret, {
                "id": auth_session.id,
                "user_id": user_id,
                "session_secret_hash": auth_session.session_secret_hash,
                "user_agent": user_agent,
                "ip_address": ip_address,
                "expires_at": expires_at.isoformat(),
            }

    def get_user_for_session_secret(self, secret: str) -> dict[str, str] | None:
        secret_hash = hash_session_secret(secret)
        with self._session() as session:
            stmt = (
                select(User, AuthSession)
                .join(AuthSession, AuthSession.user_id == User.id)
                .where(AuthSession.session_secret_hash == secret_hash)
                .where(AuthSession.revoked_at.is_(None))
            )
            row = session.execute(stmt).first()
            if row is None:
                return None
            user, auth_session = row
            if auth_session.expires_at < datetime.utcnow():
                return None
            auth_session.last_seen_at = datetime.utcnow()
            session.commit()
            return self._serialize_user(user)

    def revoke_session(self, secret: str) -> None:
        secret_hash = hash_session_secret(secret)
        with self._session() as session:
            auth_session = session.execute(
                select(AuthSession).where(AuthSession.session_secret_hash == secret_hash)
            ).scalar_one_or_none()
            if auth_session is None:
                return
            auth_session.revoked_at = datetime.utcnow()
            session.commit()

    def list_users(self) -> list[dict[str, str]]:
        with self._session() as session:
            rows = session.execute(select(User).order_by(User.created_at.asc())).scalars().all()
            return [
                {
                    "id": user.id,
                    "email": user.email,
                    "display_name": user.display_name,
                    "role": str(user.role.value if hasattr(user.role, "value") else user.role),
                    "status": user.status,
                }
                for user in rows
            ]

    def request_password_reset(self, *, email: str) -> dict[str, str] | None:
        normalized_email = email.strip().lower()
        token = mint_session_secret()
        with self._session() as session:
            user = session.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
            if user is None:
                return None
            session.add(
                PasswordResetToken(
                    user_id=user.id,
                    token_hash=hash_session_secret(token),
                    expires_at=datetime.utcnow() + timedelta(hours=1),
                )
            )
            session.commit()
            return {
                "token": token,
                "email": user.email,
                "display_name": user.display_name,
            }

    def reset_password(self, *, token: str, new_password: str) -> bool:
        token_hash = hash_session_secret(token.strip())
        now = datetime.utcnow()
        with self._session() as session:
            reset_token = session.execute(
                select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
            ).scalar_one_or_none()
            if reset_token is None or reset_token.consumed_at is not None or reset_token.expires_at < now:
                return False
            credential = session.get(UserPasswordCredential, reset_token.user_id)
            if credential is None:
                return False
            credential.password_hash = hash_password(new_password)
            credential.password_updated_at = now
            reset_token.consumed_at = now
            for auth_session in session.execute(
                select(AuthSession).where(AuthSession.user_id == reset_token.user_id)
            ).scalars():
                if auth_session.revoked_at is None:
                    auth_session.revoked_at = now
            session.commit()
            return True

    def issue_email_verification(self, *, user_id: str) -> dict[str, str] | None:
        token = mint_session_secret()
        with self._session() as session:
            user = session.get(User, user_id)
            if user is None or user.email_verified_at is not None:
                return None
            session.add(
                EmailVerificationToken(
                    user_id=user.id,
                    token_hash=hash_session_secret(token),
                    expires_at=datetime.utcnow() + timedelta(hours=24),
                )
            )
            session.commit()
            return {
                "token": token,
                "email": user.email,
                "display_name": user.display_name,
            }

    def verify_email(self, *, token: str) -> bool:
        token_hash = hash_session_secret(token.strip())
        now = datetime.utcnow()
        with self._session() as session:
            verification_token = session.execute(
                select(EmailVerificationToken).where(EmailVerificationToken.token_hash == token_hash)
            ).scalar_one_or_none()
            if (
                verification_token is None
                or verification_token.consumed_at is not None
                or verification_token.expires_at < now
            ):
                return False
            user = session.get(User, verification_token.user_id)
            if user is None:
                return False
            user.email_verified_at = now
            verification_token.consumed_at = now
            session.commit()
            return True

    def upsert_google_user(
        self,
        *,
        email: str,
        display_name: str,
        provider_subject: str,
        desired_role: str,
    ) -> dict[str, str]:
        normalized_email = email.strip().lower()
        with self._session() as session:
            identity = session.execute(
                select(UserOAuthIdentity).where(
                    UserOAuthIdentity.provider == "google",
                    UserOAuthIdentity.provider_subject == provider_subject,
                )
            ).scalar_one_or_none()
            if identity is not None:
                user = session.get(User, identity.user_id)
                if user is None:
                    raise ValueError("google_identity_without_user")
                return self._serialize_user(user)

            user = session.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
            if user is None:
                user = User(
                    email=normalized_email,
                    display_name=display_name.strip() or normalized_email,
                    role=desired_role,
                    status="active",
                    email_verified_at=datetime.utcnow(),
                )
                session.add(user)
                session.flush()

            session.add(
                UserOAuthIdentity(
                    user_id=user.id,
                    provider="google",
                    provider_subject=provider_subject,
                    email_at_link_time=normalized_email,
                )
            )
            session.commit()
            return self._serialize_user(user)
