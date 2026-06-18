import os
from collections.abc import Generator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

TEST_DATABASE_URL = (
    "postgresql+psycopg2://techuser:techpass"
    "@localhost:5434/tech_jobs_chile_test"
)

os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", TEST_DATABASE_URL)

from app.database.models import (  # noqa: E402
    Base,
    Company,
    JobPosting,
    JobPostingTechnology,
    Technology,
)
from app.database.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402


def create_company(db: Session, name: str) -> Company:
    company = Company(name=name)
    db.add(company)
    db.flush()
    return company


def create_technology(db: Session, name: str, category: str) -> Technology:
    technology = Technology(name=name, category=category)
    db.add(technology)
    db.flush()
    return technology


def create_job(
    db: Session,
    title: str,
    company: Company,
    city: str,
    modality: str,
    seniority: str,
    category: str,
    technologies: list[Technology],
    salary_min: int | None = None,
    salary_max: int | None = None,
) -> JobPosting:
    job = JobPosting(
        title=title,
        company_id=company.id,
        source="test",
        source_url=f"https://example.com/jobs/{title.lower().replace(' ', '-')}",
        city=city,
        region="Metropolitana",
        modality=modality,
        seniority=seniority,
        category=category,
        description=f"Oferta de prueba para {title}.",
        salary_min=salary_min,
        salary_max=salary_max,
        salary_currency="CLP",
        published_at=date(2026, 6, 1),
        collected_at=date(2026, 6, 18),
    )

    db.add(job)
    db.flush()

    for technology in technologies:
        db.add(
            JobPostingTechnology(
                job_posting_id=job.id,
                technology_id=technology.id,
            )
        )

    return job


def seed_test_database(db: Session) -> None:
    backend_company = create_company(db, "Backend Test SpA")
    frontend_company = create_company(db, "Frontend Test SpA")
    data_company = create_company(db, "Data Test SpA")

    python = create_technology(db, "Python", "Language")
    fastapi = create_technology(db, "FastAPI", "Backend")
    postgresql = create_technology(db, "PostgreSQL", "Database")
    react = create_technology(db, "React", "Frontend")
    typescript = create_technology(db, "TypeScript", "Language")
    sql = create_technology(db, "SQL", "Database")
    power_bi = create_technology(db, "Power BI", "Data")
    docker = create_technology(db, "Docker", "DevOps")

    create_job(
        db=db,
        title="Backend Developer Python",
        company=backend_company,
        city="Santiago",
        modality="hibrido",
        seniority="junior",
        category="backend",
        technologies=[python, fastapi, postgresql, docker],
        salary_min=900_000,
        salary_max=1_300_000,
    )

    create_job(
        db=db,
        title="Frontend Developer React",
        company=frontend_company,
        city="Remote",
        modality="remoto",
        seniority="junior",
        category="frontend",
        technologies=[react, typescript],
        salary_min=850_000,
        salary_max=1_250_000,
    )

    create_job(
        db=db,
        title="Data Analyst Junior",
        company=data_company,
        city="Santiago",
        modality="remoto",
        seniority="junior",
        category="data",
        technologies=[sql, python, power_bi],
        salary_min=800_000,
        salary_max=1_200_000,
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        seed_test_database(db)
        db.commit()
    finally:
        db.close()

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(setup_test_database: None) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client