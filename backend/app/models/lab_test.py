"""LabTest model."""

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.models.mixins import TimestampMixin


class LabTest(Base, TimestampMixin):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
