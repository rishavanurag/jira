"""seed system member role

Revision ID: bee38f87b574
Revises: 2ced0b347ad6
Create Date: 2026-08-19 23:41:58.681581

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision: str = "bee38f87b574"
down_revision: Union[str, Sequence[str], None] = "2ced0b347ad6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ROLE_ID = "b1c6a97c-a7d3-4f2d-b0e0-0a841856837f"


def upgrade() -> None:
    """Upgrade schema."""
    insert_query = sa.text(
        "INSERT INTO roles (id, code, name, description, is_system, is_active, created_at) VALUES (:id, :code, :name, :description, :is_system, :is_active, :created_at)"
    ).bindparams(
        id=ROLE_ID,
        code="MEMBER",
        name="Member",
        description="System role member",
        is_system=True,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    op.execute(insert_query)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM roles WHERE id = :id").bindparams(id=ROLE_ID))
