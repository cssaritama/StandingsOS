import os

APP_NAME = "StandingsOS API"
APP_VERSION = "2.2.1"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./standingsos.db")

DEFAULT_CORS_ORIGINS = (
    "http://localhost:5173,http://127.0.0.1:5173,"
    "http://localhost:8080,http://127.0.0.1:8080"
)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]

AUTO_CREATE_SCHEMA = os.getenv("AUTO_CREATE_SCHEMA", "true").lower() in {"1", "true", "yes"}
SEED_DEMO_DATA = os.getenv("SEED_DEMO_DATA", "false").lower() in {"1", "true", "yes"}

AI_PROVIDER = os.getenv("AI_PROVIDER", "disabled").strip().lower()
AI_MODEL = os.getenv("AI_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434").rstrip("/")
AI_TIMEOUT_SECONDS = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))
