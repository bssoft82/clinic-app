"""PrescriptionTemplate model and its sub-tables."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.enums import Prerequisite
from app.models.mixins import TimestampMixin


class PrescriptionTemplate(Base, TimestampMixin):
    __tablename__ = "prescription_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # Doctor-assigned tag (English)

    # Relationships
    symptom_links = relationship("PrescriptionTemplateSymptom", back_populates="template", cascade="all, delete-orphan")
    medicines = relationship("PrescriptionTemplateMedicine", back_populates="template", cascade="all, delete-orphan")
    advice = relationship("PrescriptionTemplateAdvice", back_populates="template", cascade="all, delete-orphan")
    lab_test_links = relationship("PrescriptionTemplateLabTest", back_populates="template", cascade="all, delete-orphan")


class PrescriptionTemplateSymptom(Base):
    """Association table linking templates to symptoms (for recommendation matching)."""
    __tablename__ = "prescription_template_symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_template_id = Column(Integer, ForeignKey("prescription_templates.id", ondelete="CASCADE"), nullable=False)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), nullable=False)

    template = relationship("PrescriptionTemplate", back_populates="symptom_links")


class PrescriptionTemplateMedicine(Base):
    """Medicine entry within a prescription template (with per-template overrides)."""
    __tablename__ = "prescription_template_medicines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_template_id = Column(Integer, ForeignKey("prescription_templates.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    duration_days = Column(Integer, nullable=False, default=5)
    dose_times = Column(String, nullable=True, default="MORNING,NIGHT")
    prerequisite = Column(Enum(Prerequisite), nullable=True)

    template = relationship("PrescriptionTemplate", back_populates="medicines")


class PrescriptionTemplateAdvice(Base):
    """Advice text within a prescription template."""
    __tablename__ = "prescription_template_advice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_template_id = Column(Integer, ForeignKey("prescription_templates.id", ondelete="CASCADE"), nullable=False)
    advice_text = Column(Text, nullable=False)

    template = relationship("PrescriptionTemplate", back_populates="advice")


class PrescriptionTemplateLabTest(Base):
    """Association table linking templates to lab tests."""
    __tablename__ = "prescription_template_lab_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_template_id = Column(Integer, ForeignKey("prescription_templates.id", ondelete="CASCADE"), nullable=False)
    lab_test_id = Column(Integer, ForeignKey("lab_tests.id"), nullable=False)

    template = relationship("PrescriptionTemplate", back_populates="lab_test_links")
