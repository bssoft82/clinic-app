"""Symptom model."""

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.models.mixins import TimestampMixin


class Symptom(Base, TimestampMixin):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
