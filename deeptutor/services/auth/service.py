from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from deeptutor.services.auth.models import AuthSession
from deeptutor.services.auth.models import User
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
            return {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "role": str(user.role.value if hasattr(user.role, "value") else user.role),
            }

    def authenticate_user(self, *, email: str, password: str) -> dict[str, str] | None:
        normalized_email = email.strip().lower()
        with self._session() as session:
            user = session.execute(select(User).where(User.email == normalized_email)).scalar_one_or_none()
            if user is None:
                return None
            credential = session.get(UserPasswordCredential, user.id)
            if credential is None or not verify_password(password, credential.password_hash):
                return None
            return {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "role": str(user.role.value if hasattr(user.role, "value") else user.role),
            }

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
            return {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "role": str(user.role.value if hasattr(user.role, "value") else user.role),
            }

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
