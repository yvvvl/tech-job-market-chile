import csv
from datetime import date

from sqlalchemy.orm import Session

from app.core.config import ROOT_DIR
from app.database.models import Company, JobPosting, JobPostingTechnology, Technology
from app.database.session import SessionLocal
from app.pipeline.tech_rules import (
    TECHNOLOGIES,
    extract_technologies,
    infer_job_category,
    infer_modality,
    infer_seniority,
)

CSV_PATH = ROOT_DIR / "data" / "seeds" / "sample_postings.csv"


def parse_int(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    return int(value.strip())


def parse_date(value: str | None) -> date | None:
    if value is None or value.strip() == "":
        return None
    return date.fromisoformat(value.strip())


def get_or_create_company(db: Session, name: str) -> Company:
    company = db.query(Company).filter(Company.name == name).first()
    if company:
        return company

    company = Company(name=name)
    db.add(company)
    db.flush()
    return company


def get_or_create_technology(db: Session, name: str) -> Technology:
    technology = db.query(Technology).filter(Technology.name == name).first()
    if technology:
        return technology

    technology = Technology(name=name, category=TECHNOLOGIES.get(name, "Other"))
    db.add(technology)
    db.flush()
    return technology


def clear_database(db: Session) -> None:
    db.query(JobPostingTechnology).delete()
    db.query(JobPosting).delete()
    db.query(Technology).delete()
    db.query(Company).delete()
    db.commit()


def seed_database() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo: {CSV_PATH}")

    db = SessionLocal()

    try:
        clear_database(db)

        with CSV_PATH.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            inserted = 0

            for row in reader:
                title = row["title"].strip()
                description = row["description"].strip()
                company = get_or_create_company(db, row["company"].strip())
                techs = extract_technologies(f"{title} {description}")

                posting = JobPosting(
                    title=title,
                    company_id=company.id,
                    city=row.get("city", "").strip() or None,
                    modality=infer_modality(title, description, row.get("modality")),
                    seniority=infer_seniority(title, description, row.get("seniority")),
                    category=infer_job_category(title, description, techs),
                    description=description,
                    salary_min=parse_int(row.get("salary_min")),
                    salary_max=parse_int(row.get("salary_max")),
                    published_at=parse_date(row.get("published_at")),
                    source=row.get("source", "manual").strip() or "manual",
                )

                db.add(posting)
                db.flush()

                for tech_name in techs:
                    technology = get_or_create_technology(db, tech_name)
                    db.add(
                        JobPostingTechnology(
                            job_posting_id=posting.id,
                            technology_id=technology.id,
                        )
                    )

                inserted += 1

        db.commit()
        print(f"Seed cargado correctamente: {inserted} ofertas insertadas desde {CSV_PATH}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
