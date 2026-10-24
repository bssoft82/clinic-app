"""Reusable mixins for SQLAlchemy models."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime


class TimestampMixin:
    """Adds created_at and updated_at columns to a model."""

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
