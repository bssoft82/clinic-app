"""Enum definitions for database models."""

import enum


class MedicineType(enum.Enum):
    FLUID = "Fluid"
    CAPSULE = "Capsule"
    TABLET = "Tablet"
    INJECTION = "Injection"


class DoseTime(enum.Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"
    NIGHT = "NIGHT"

    @property
    def marathi(self) -> str:
        return {
            DoseTime.MORNING: "सकाळी",
            DoseTime.AFTERNOON: "दुपारी",
            DoseTime.EVENING: "संध्याकाळी",
            DoseTime.NIGHT: "रात्री",
        }[self]


class Prerequisite(enum.Enum):
    AFTER_FOOD = "AFTER_FOOD"
    BEFORE_FOOD = "BEFORE_FOOD"
    EMPTY_STOMACH = "EMPTY_STOMACH"
    NONE = "NONE"

    @property
    def english(self) -> str:
        return {
            Prerequisite.AFTER_FOOD: "After Food",
            Prerequisite.BEFORE_FOOD: "Before Food",
            Prerequisite.EMPTY_STOMACH: "Empty Stomach",
            Prerequisite.NONE: "None",
        }[self]

    @property
    def marathi(self) -> str:
        return {
            Prerequisite.AFTER_FOOD: "जेवणानंतर",
            Prerequisite.BEFORE_FOOD: "जेवणापूर्वी",
            Prerequisite.EMPTY_STOMACH: "रिकाम्या पोटी",
            Prerequisite.NONE: "काहीही नाही",
        }[self]

    @property
    def display(self) -> str:
        """Combined English + Marathi display."""
        return f"{self.english} / {self.marathi}"


class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
