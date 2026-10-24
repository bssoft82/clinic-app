"""Prescription model and its sub-tables."""

from datetime import date as date_type

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Prerequisite
from app.models.mixins import TimestampMixin


class Prescription(Base, TimestampMixin):
    """A prescription is immutable after creation (no edit/delete)."""
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(Date, nullable=False)
    patient_type = Column(String, nullable=False, default="OPD")

    # Optional diagnosis (illness reference)
    illness_id = Column(Integer, ForeignKey("illnesses.id"), nullable=True)

    # Vital signs (all optional)
    blood_pressure = Column(String, nullable=True)   # e.g., "120/80"
    temperature = Column(String, nullable=True)        # e.g., "98.6"
    spo2 = Column(String, nullable=True)               # e.g., "98"
    pulse = Column(String, nullable=True)              # e.g., "72"

    # Relationships
    patient = relationship("Patient")
    illness = relationship("Illness")
    symptom_links = relationship("PrescriptionSymptom", back_populates="prescription", cascade="all, delete-orphan")
    medicines = relationship("PrescriptionMedicine", back_populates="prescription", cascade="all, delete-orphan")
    advice = relationship("PrescriptionAdvice", back_populates="prescription", cascade="all, delete-orphan")
    lab_test_links = relationship("PrescriptionLabTest", back_populates="prescription", cascade="all, delete-orphan")
    referral_links = relationship("PrescriptionReferral", back_populates="prescription", cascade="all, delete-orphan")


class PrescriptionSymptom(Base):
    """Association table linking prescriptions to symptoms."""
    __tablename__ = "prescription_symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), nullable=False)

    prescription = relationship("Prescription", back_populates="symptom_links")


class PrescriptionMedicine(Base):
    """Medicine entry within a prescription (with per-Rx overrides)."""
    __tablename__ = "prescription_medicines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    duration_days = Column(Integer, nullable=False, default=5)
    dose_times = Column(String, nullable=True, default="MORNING,NIGHT")
    prerequisite = Column(Enum(Prerequisite), nullable=True)

    prescription = relationship("Prescription", back_populates="medicines")
    medicine = relationship("Medicine")


class PrescriptionAdvice(Base):
    """Advice text within a prescription (Marathi free text)."""
    __tablename__ = "prescription_advice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    advice_text = Column(Text, nullable=False)

    prescription = relationship("Prescription", back_populates="advice")


class PrescriptionLabTest(Base):
    """Association table linking prescriptions to lab tests."""
    __tablename__ = "prescription_lab_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    lab_test_id = Column(Integer, ForeignKey("lab_tests.id"), nullable=False)

    prescription = relationship("Prescription", back_populates="lab_test_links")


class PrescriptionReferral(Base):
    """Association table linking prescriptions to referral doctors."""
    __tablename__ = "prescription_referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    referral_doctor_id = Column(Integer, ForeignKey("referral_doctors.id"), nullable=False)

    prescription = relationship("Prescription", back_populates="referral_links")
