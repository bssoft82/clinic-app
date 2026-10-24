"""Application configuration."""

from pathlib import Path

# Base directory is backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database file lives in the backend directory
DATABASE_URL = f"sqlite:///{BASE_DIR / 'clinic.db'}"

# API prefix for all routes
API_V1_PREFIX = "/api/v1"
