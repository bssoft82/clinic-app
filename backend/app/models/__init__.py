"""SQLAlchemy models package.

Importing this package registers all models with the Base metadata,
which is required for Alembic migrations and table creation.
"""

from app.models.enums import MedicineType, DoseTime, Prerequisite, Gender
from app.models.mixins import TimestampMixin
from app.models.illness import Illness
from app.models.medicine import Medicine
from app.models.patient import Patient
from app.models.lab_test import LabTest
from app.models.symptom import Symptom
from app.models.referral_doctor import ReferralDoctor
from app.models.advice_template import AdviceTemplate
from app.models.prescription_template import (
    PrescriptionTemplate,
    PrescriptionTemplateSymptom,
    PrescriptionTemplateMedicine,
    PrescriptionTemplateAdvice,
    PrescriptionTemplateLabTest,
)
from app.models.prescription import (
    Prescription,
    PrescriptionSymptom,
    PrescriptionMedicine,
    PrescriptionAdvice,
    PrescriptionLabTest,
    PrescriptionReferral,
)

__all__ = [
    "Illness",
    "Medicine",
    "Patient",
    "LabTest",
    "Symptom",
    "ReferralDoctor",
    "AdviceTemplate",
    "PrescriptionTemplate",
    "PrescriptionTemplateSymptom",
    "PrescriptionTemplateMedicine",
    "PrescriptionTemplateAdvice",
    "PrescriptionTemplateLabTest",
    "Prescription",
    "PrescriptionSymptom",
    "PrescriptionMedicine",
    "PrescriptionAdvice",
    "PrescriptionLabTest",
    "PrescriptionReferral",
    "MedicineType",
    "DoseTime",
    "Prerequisite",
    "Gender",
]
