import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.organization import Membership


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    memberships: Mapped[List["Membership"]] = relationship(
        "Membership", back_populates="user", foreign_keys="Membership.user_id"
    )

    @validates("full_name")
    def validate_full_name(self, key: str, full_name: str) -> str:
        """remove leading and trailing whitespace from full name."""
        return full_name.strip()

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        """convert email address to lower case."""
        return email.strip().lower()
