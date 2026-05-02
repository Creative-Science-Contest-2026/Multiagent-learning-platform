from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field


class AuthDatabaseSettings(BaseModel):
    database_url: str = Field(..., min_length=1)


@lru_cache(maxsize=1)
def get_auth_engine(database_url: str) -> Any:
    from sqlalchemy import create_engine

    return create_engine(database_url, future=True, pool_pre_ping=True)
