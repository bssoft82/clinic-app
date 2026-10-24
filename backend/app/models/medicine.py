"""Medicine model."""

from sqlalchemy import Column, Enum, Integer, String

from app.database import Base
from app.models.enums import MedicineType, DoseTime, Prerequisite
from app.models.mixins import TimestampMixin

# dose_times is stored as a JSON array string of DoseTime enum values


class Medicine(Base, TimestampMixin):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    medicine_type = Column(Enum(MedicineType), nullable=False, default=MedicineType.TABLET)
    default_duration_days = Column(Integer, nullable=False, default=5)
    # Stored as comma-separated enum names, e.g. "MORNING,NIGHT"
    dose_times = Column(String, nullable=True, default="MORNING,NIGHT")
    prerequisite = Column(Enum(Prerequisite), nullable=True)
