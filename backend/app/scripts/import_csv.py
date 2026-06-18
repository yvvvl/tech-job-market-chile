import argparse
import csv
import re
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.models import Company, JobPosting, JobPostingTechnology, Technology
from app.database.session import SessionLocal
from app.pipeline.tech_rules import (
    TECHNOLOGIES,
    extract_technologies,
    infer_job_category,
    infer_modality,
    infer_seniority,
)


REQUIRED_COLUMNS = {
    "source",
    "source_url",
    "title",
    "company",
    "city",
    "region",
    "modality",
    "seniority",
    "category",
    "description",
    "technologies_raw",
    "salary_min",
    "salary_max",
    "salary_currency",
    "published_at",
    "collected_at",
}


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned if cleaned else None


def parse_int(value: str | None) -> int | None:
    value = clean_text(value)

    if not value:
        return None

    cleaned = (
        value.replace(".", "")
        .replace(",", "")
        .replace("$", "")
        .replace("CLP", "")
        .replace("USD", "")
        .strip()
    )

    if not cleaned:
        return None

    if not cleaned.isdigit():
        raise ValueError(
            f"Valor numérico inválido para salario: '{value}'. "
            "Probablemente el CSV quedó desalineado por una coma sin comillas. "
            "Revisa esa fila."
        )

    return int(cleaned)


def parse_date(value: str | None) -> date | None:
    value = clean_text(value)

    if not value:
        return None

    return date.fromisoformat(value)


def split_technologies(raw: str | None) -> list[str]:
    raw = clean_text(raw)

    if not raw:
        return []

    parts = re.split(r"[;,\n|]+", raw)
    technologies: list[str] = []

    for part in parts:
        cleaned = clean_text(part)

        if not cleaned:
            continue

        cleaned = cleaned.strip('"').strip("'").strip()

        if cleaned:
            technologies.append(cleaned)

    return sorted(set(technologies))


def normalize_technology_list(items: list[str]) -> list[str]:
    normalized: set[str] = set()

    for item in items:
        for part in split_technologies(item):
            cleaned = clean_text(part)

            if not cleaned:
                continue

            if len(cleaned) > 180:
                print(f"⚠️ Tecnología omitida por largo excesivo: {cleaned[:100]}...")
                continue

            normalized.add(cleaned)

    return sorted(normalized)


def normalize_slug(value: str | None, default: str = "unknown") -> str:
    cleaned = clean_text(value)

    if not cleaned:
        return default

    return (
        cleaned.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace(" ", "_")
        .replace("-", "_")
    )


def validate_columns(headers: list[str] | None) -> None:
    if headers is None:
        raise ValueError("El CSV no tiene encabezados.")

    missing = REQUIRED_COLUMNS - set(headers)

    if missing:
        raise ValueError(
            "Faltan columnas requeridas en el CSV: "
            + ", ".join(sorted(missing))
        )


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

    technology = Technology(
        name=name,
        category=TECHNOLOGIES.get(name, "Other"),
    )

    db.add(technology)
    db.flush()

    return technology


def clear_database(db: Session) -> None:
    db.query(JobPostingTechnology).delete()
    db.query(JobPosting).delete()
    db.query(Technology).delete()
    db.query(Company).delete()
    db.commit()


def job_exists(db: Session, source_url: str | None, title: str, company_id: int | None) -> bool:
    if company_id is None:
        return False

    if source_url:
        existing_by_url = (
            db.query(JobPosting)
            .filter(JobPosting.source_url == source_url)
            .first()
        )

        if existing_by_url:
            return True

    existing_by_title_company = (
        db.query(JobPosting)
        .filter(
            JobPosting.title == title,
            JobPosting.company_id == company_id,
        )
        .first()
    )

    return existing_by_title_company is not None


def validate_row_shape(row: dict, line_num: int) -> None:
    if None in row:
        raise ValueError(
            f"Fila CSV mal formada en línea {line_num}. "
            f"Hay columnas extra probablemente por comas sin comillas: {row[None]}. "
            "Solución: si un campo tiene coma, encierra ese campo entre comillas dobles."
        )


def import_csv(file_path: Path, replace: bool = False) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")

    db = SessionLocal()

    try:
        if replace:
            clear_database(db)

        inserted = 0
        skipped = 0

        with file_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            validate_columns(reader.fieldnames)

            for row in reader:
                validate_row_shape(row, reader.line_num)

                title = clean_text(row.get("title"))

                if not title:
                    skipped += 1
                    continue

                company_name = clean_text(row.get("company")) or "Unknown"
                company = get_or_create_company(db, company_name)

                source_url = clean_text(row.get("source_url"))

                if job_exists(db, source_url, title, company.id):
                    skipped += 1
                    continue

                description = clean_text(row.get("description")) or ""

                technologies_raw = split_technologies(row.get("technologies_raw"))

                detected_technologies = extract_technologies(
                    " ".join([title, description, " ".join(technologies_raw)])
                )

                technologies = normalize_technology_list(
                    technologies_raw + detected_technologies
                )

                seniority = clean_text(row.get("seniority")) or infer_seniority(
                    title,
                    description,
                )

                modality = clean_text(row.get("modality")) or infer_modality(
                    title,
                    description,
                )

                category = clean_text(row.get("category")) or infer_job_category(
                    title,
                    description,
                    technologies,
                )

                posting = JobPosting(
                    title=title,
                    company_id=company.id,
                    source=clean_text(row.get("source")) or "manual",
                    source_url=source_url,
                    city=clean_text(row.get("city")),
                    region=clean_text(row.get("region")),
                    modality=normalize_slug(modality),
                    seniority=normalize_slug(seniority),
                    category=normalize_slug(category, default="other"),
                    description=description,
                    salary_min=parse_int(row.get("salary_min")),
                    salary_max=parse_int(row.get("salary_max")),
                    salary_currency=clean_text(row.get("salary_currency")),
                    published_at=parse_date(row.get("published_at")),
                    collected_at=parse_date(row.get("collected_at")),
                )

                db.add(posting)
                db.flush()

                for tech_name in technologies:
                    technology = get_or_create_technology(db, tech_name)

                    db.add(
                        JobPostingTechnology(
                            job_posting_id=posting.id,
                            technology_id=technology.id,
                        )
                    )

                inserted += 1

        db.commit()

        print("✅ Importación completada.")
        print(f"Archivo: {file_path}")
        print(f"Insertadas: {inserted}")
        print(f"Saltadas: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Importar ofertas laborales desde CSV.")
    parser.add_argument("file", type=Path, help="Ruta al archivo CSV.")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Borra los datos actuales antes de importar.",
    )

    args = parser.parse_args()
    import_csv(args.file, replace=args.replace)


if __name__ == "__main__":
    main()