"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_V1_PREFIX

app = FastAPI(
    title="Clinic Prescription API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow the Vite dev server to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{API_V1_PREFIX}/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
