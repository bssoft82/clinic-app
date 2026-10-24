"""Illness model."""

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.models.mixins import TimestampMixin


class Illness(Base, TimestampMixin):
    __tablename__ = "illnesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
