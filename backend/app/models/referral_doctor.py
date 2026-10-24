"""ReferralDoctor model."""

from sqlalchemy import Column, Integer, String

from app.database import Base
from app.models.mixins import TimestampMixin


class ReferralDoctor(Base, TimestampMixin):
    __tablename__ = "referral_doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
