"""Patient model."""

from sqlalchemy import Column, Enum, Integer, String

from app.database import Base
from app.models.enums import Gender
from app.models.mixins import TimestampMixin


class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)          # English, used for search
    name_marathi = Column(String, nullable=True)    # Marathi, displayed alongside
    gender = Column(Enum(Gender), nullable=True)
    age = Column(Integer, nullable=True)
    mobile_number = Column(String, nullable=True)
    residence = Column(String, nullable=True)
