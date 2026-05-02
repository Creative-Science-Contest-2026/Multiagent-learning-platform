from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from deeptutor.services.path_service import get_path_service


class AuthDatabaseSettings(BaseModel):
    database_url: str = Field(..., min_length=1)


@lru_cache(maxsize=1)
def get_auth_database_url() -> str:
    configured = os.getenv("DEEPTUTOR_AUTH_DATABASE_URL", "").strip()
    if configured:
        return configured
    path: Path = get_path_service().get_user_root() / "auth.db"
    return f"sqlite+pysqlite:///{path}"


@lru_cache(maxsize=4)
def get_auth_engine(database_url: str | None = None) -> Any:
    from sqlalchemy import create_engine

    resolved_url = database_url or get_auth_database_url()
    connect_args = {"check_same_thread": False} if resolved_url.startswith("sqlite") else {}
    return create_engine(resolved_url, future=True, pool_pre_ping=True, connect_args=connect_args)


@lru_cache(maxsize=4)
def get_auth_session_factory(database_url: str | None = None) -> Any:
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=get_auth_engine(database_url), autoflush=False, autocommit=False, future=True)


def init_auth_schema(database_url: str | None = None) -> None:
    from deeptutor.services.auth.models import Base

    Base.metadata.create_all(bind=get_auth_engine(database_url))


def clear_auth_database_caches() -> None:
    get_auth_database_url.cache_clear()
    get_auth_engine.cache_clear()
    get_auth_session_factory.cache_clear()
