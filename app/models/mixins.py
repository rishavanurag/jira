from datetime import datetime, timezone
from sqlalchemy import Column, DateTime

class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps to a model."""

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))
