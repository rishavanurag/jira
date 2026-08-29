"""seed system owner role

Revision ID: 2ced0b347ad6
Revises: dd1538c6d116
Create Date: 2026-08-10 00:44:37.008353

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

# revision identifiers, used by Alembic.
revision: str = "2ced0b347ad6"
down_revision: Union[str, Sequence[str], None] = "dd1538c6d116"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ROLE_ID = "e21f76fc-76ad-46c5-8436-92ac5501982c"


def upgrade() -> None:
    """Upgrade schema."""
    insert_query = sa.text(
        "INSERT INTO roles (id, code, name, description, is_system, is_active, created_at) VALUES (:id, :code, :name, :description, :is_system, :is_active, :created_at)"
    ).bindparams(
        id=ROLE_ID,
        code="OWNER",
        name="Owner",
        description="System role owner",
        is_system=True,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    op.execute(insert_query)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM roles WHERE id = :id").bindparams(id=ROLE_ID))
