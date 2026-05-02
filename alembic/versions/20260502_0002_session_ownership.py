"""Add owner tracking to unified sessions."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260502_0002"
down_revision = "20260502_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sessions", sa.Column("owner_user_id", sa.String(length=36), nullable=True))


def downgrade() -> None:
    op.drop_column("sessions", "owner_user_id")
