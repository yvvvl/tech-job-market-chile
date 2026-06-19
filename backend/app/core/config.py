import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / ".env")


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://techuser:techpass@localhost:5433/tech_jobs_chile"
    )
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    app_name: str = os.getenv("APP_NAME", "Tech Jobs Chile API")


settings = Settings()
