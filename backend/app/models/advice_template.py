"""AdviceTemplate model."""

from sqlalchemy import Column, Integer, String, Text

from app.database import Base
from app.models.mixins import TimestampMixin


class AdviceTemplate(Base, TimestampMixin):
    __tablename__ = "advice_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
