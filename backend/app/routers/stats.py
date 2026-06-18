from collections import defaultdict
from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, Query as ApiQuery
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database.models import Company, JobPosting, JobPostingTechnology, Technology
from app.database.session import get_db


router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])


SENIORITY_LABELS = {
    "trainee": "Trainee",
    "junior": "Junior",
    "semi_senior": "Semi-Senior",
    "senior": "Senior",
    "lead": "Lead",
    "principal": "Principal",
    "unknown": "Unknown",
}


SENIORITY_COLORS = {
    "trainee": "var(--color-chart-2)",
    "junior": "var(--color-chart-2)",
    "semi_senior": "var(--color-chart-1)",
    "senior": "var(--color-chart-3)",
    "lead": "var(--color-chart-3)",
    "principal": "var(--color-chart-3)",
    "unknown": "var(--color-chart-4)",
}


def normalize_slug(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()

    if not cleaned:
        return None

    return (
        cleaned.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("-", "_")
        .replace(" ", "_")
    )


def build_filters(
    seniority: str | None = ApiQuery(default=None, description="Ej: junior, trainee, senior"),
    category: str | None = ApiQuery(default=None, description="Ej: backend, frontend, data, devops"),
    city: str | None = ApiQuery(default=None, description="Ej: Santiago, Remote, Concepción"),
    modality: str | None = ApiQuery(default=None, description="Ej: remoto, hibrido, presencial"),
    source: str | None = ApiQuery(default=None, description="Ej: LinkedIn, GetOnBoard, Laborum"),
    from_date: date | None = ApiQuery(default=None, description="Fecha inicial YYYY-MM-DD"),
    to_date: date | None = ApiQuery(default=None, description="Fecha final YYYY-MM-DD"),
) -> dict[str, Any]:
    return {
        "seniority": seniority,
        "category": category,
        "city": city,
        "modality": modality,
        "source": source,
        "from_date": from_date,
        "to_date": to_date,
    }


def serialize_filters(filters: dict[str, Any]) -> dict[str, str]:
    serialized: dict[str, str] = {}

    for key, value in filters.items():
        if value is None:
            continue

        if isinstance(value, date):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = str(value)

    return serialized


def apply_job_filters(query, filters: dict[str, Any]):
    seniority = normalize_slug(filters.get("seniority"))
    category = normalize_slug(filters.get("category"))
    modality = normalize_slug(filters.get("modality"))
    city = filters.get("city")
    source = filters.get("source")
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    if seniority:
        query = query.filter(JobPosting.seniority == seniority)

    if category:
        query = query.filter(JobPosting.category == category)

    if modality:
        query = query.filter(JobPosting.modality == modality)

    if city:
        query = query.filter(func.lower(JobPosting.city) == city.strip().lower())

    if source:
        query = query.filter(func.lower(JobPosting.source) == source.strip().lower())

    date_expr = func.coalesce(JobPosting.published_at, JobPosting.collected_at)

    if from_date:
        query = query.filter(date_expr >= from_date)

    if to_date:
        query = query.filter(date_expr <= to_date)

    return query


def salary_midpoint_expression():
    return (
        func.coalesce(JobPosting.salary_min, JobPosting.salary_max)
        + func.coalesce(JobPosting.salary_max, JobPosting.salary_min)
    ) / 2.0


def count_filtered_jobs(db: Session, filters: dict[str, Any]) -> int:
    query = db.query(func.count(JobPosting.id))
    query = apply_job_filters(query, filters)

    return int(query.scalar() or 0)


def get_technology_rows(
    db: Session,
    filters: dict[str, Any],
    limit: int = 30,
) -> list[dict]:
    salary_mid = salary_midpoint_expression()

    junior_case = case(
        (JobPosting.seniority.in_(["trainee", "junior"]), 1),
        else_=0,
    )

    query = (
        db.query(
            Technology.name.label("name"),
            Technology.category.label("category"),
            func.count(JobPostingTechnology.job_posting_id).label("demand"),
            func.sum(junior_case).label("junior_count"),
            func.avg(salary_mid).label("avg_salary"),
        )
        .join(JobPostingTechnology, JobPostingTechnology.technology_id == Technology.id)
        .join(JobPosting, JobPosting.id == JobPostingTechnology.job_posting_id)
    )

    query = apply_job_filters(query, filters)

    rows = (
        query.group_by(Technology.id, Technology.name, Technology.category)
        .order_by(func.count(JobPostingTechnology.job_posting_id).desc())
        .limit(limit)
        .all()
    )

    result = []

    for row in rows:
        demand = int(row.demand or 0)
        junior_count = int(row.junior_count or 0)
        junior_friendly = round((junior_count / demand) * 100) if demand else 0
        avg_salary = int(row.avg_salary or 0)

        result.append(
            {
                "name": row.name,
                "category": row.category,
                "demand": demand,
                "trend": 0,
                "juniorFriendly": junior_friendly,
                "avgSalaryCLP": avg_salary,
                "related": [],
            }
        )

    by_category: dict[str, list[str]] = defaultdict(list)

    for item in result:
        by_category[item["category"]].append(item["name"])

    for item in result:
        item["related"] = [
            name for name in by_category[item["category"]] if name != item["name"]
        ][:4]

    return result


def get_cities_rows(db: Session, filters: dict[str, Any]) -> list[dict]:
    query = db.query(
        JobPosting.city.label("city"),
        func.count(JobPosting.id).label("job_count"),
    )

    query = apply_job_filters(query, filters)

    rows = (
        query.group_by(JobPosting.city)
        .order_by(func.count(JobPosting.id).desc())
        .all()
    )

    return [
        {
            "city": row.city or "Unknown",
            "jobs": int(row.job_count or 0),
        }
        for row in rows
    ]


def get_seniority_rows(db: Session, filters: dict[str, Any]) -> list[dict]:
    query = db.query(
        JobPosting.seniority.label("seniority"),
        func.count(JobPosting.id).label("job_count"),
    )

    query = apply_job_filters(query, filters)

    rows = (
        query.group_by(JobPosting.seniority)
        .order_by(func.count(JobPosting.id).desc())
        .all()
    )

    return [
        {
            "level": SENIORITY_LABELS.get(
                row.seniority or "unknown",
                row.seniority or "Unknown",
            ),
            "count": int(row.job_count or 0),
            "fill": SENIORITY_COLORS.get(
                row.seniority or "unknown",
                "var(--color-chart-4)",
            ),
        }
        for row in rows
    ]


def get_category_breakdown(db: Session, filters: dict[str, Any]) -> list[dict]:
    query = db.query(
        JobPosting.category.label("category"),
        func.count(JobPosting.id).label("demand"),
    )

    query = apply_job_filters(query, filters)

    rows = (
        query.group_by(JobPosting.category)
        .order_by(func.count(JobPosting.id).desc())
        .all()
    )

    return [
        {
            "category": row.category or "unknown",
            "demand": int(row.demand or 0),
        }
        for row in rows
    ]


def get_salary_ranges(db: Session, filters: dict[str, Any]) -> list[dict]:
    query = db.query(JobPosting.salary_min, JobPosting.salary_max)
    query = apply_job_filters(query, filters)

    salaries = []

    for posting in query.all():
        if posting.salary_min is None and posting.salary_max is None:
            continue

        min_salary = posting.salary_min or posting.salary_max
        max_salary = posting.salary_max or posting.salary_min
        salaries.append((min_salary + max_salary) / 2)

    ranges = [
        ("< 1M", 0, 1_000_000),
        ("1M – 1.5M", 1_000_000, 1_500_000),
        ("1.5M – 2M", 1_500_000, 2_000_000),
        ("2M – 2.5M", 2_000_000, 2_500_000),
        ("2.5M – 3M", 2_500_000, 3_000_000),
        ("3M – 4M", 3_000_000, 4_000_000),
        ("> 4M", 4_000_000, float("inf")),
    ]

    return [
        {
            "range": label,
            "count": sum(1 for salary in salaries if lower <= salary < upper),
        }
        for label, lower, upper in ranges
    ]


def get_monthly_trend(db: Session, filters: dict[str, Any]) -> list[dict]:
    date_expr = func.coalesce(JobPosting.published_at, JobPosting.collected_at)
    month_expr = func.date_trunc("month", date_expr)

    junior_case = case(
        (JobPosting.seniority.in_(["trainee", "junior"]), 1),
        else_=0,
    )

    query = db.query(
        func.to_char(month_expr, "Mon").label("month"),
        func.count(JobPosting.id).label("jobs"),
        func.sum(junior_case).label("junior"),
        month_expr.label("month_date"),
    ).filter(date_expr.isnot(None))

    query = apply_job_filters(query, filters)

    rows = (
        query.group_by(month_expr)
        .order_by(month_expr)
        .all()
    )

    return [
        {
            "month": row.month.strip(),
            "jobs": int(row.jobs or 0),
            "junior": int(row.junior or 0),
        }
        for row in rows
    ]


def get_stats_summary(db: Session, filters: dict[str, Any]) -> dict:
    jobs_query = db.query(JobPosting)
    jobs_query = apply_job_filters(jobs_query, filters)

    company_query = db.query(func.count(func.distinct(JobPosting.company_id)))
    company_query = apply_job_filters(company_query, filters)

    tech_query = (
        db.query(func.count(func.distinct(Technology.id)))
        .join(JobPostingTechnology, JobPostingTechnology.technology_id == Technology.id)
        .join(JobPosting, JobPosting.id == JobPostingTechnology.job_posting_id)
    )
    tech_query = apply_job_filters(tech_query, filters)

    city_query = db.query(func.count(func.distinct(JobPosting.city)))
    city_query = apply_job_filters(city_query, filters)

    return {
        "totalJobs": int(jobs_query.count() or 0),
        "companies": int(company_query.scalar() or 0),
        "technologies": int(tech_query.scalar() or 0),
        "cities": int(city_query.scalar() or 0),
    }


@router.get("/overview")
def get_overview(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
):
    return {
        "stats": get_stats_summary(db, filters),
        "monthlyTrend": get_monthly_trend(db, filters),
        "technologies": get_technology_rows(db, filters, limit=30),
        "categoryBreakdown": get_category_breakdown(db, filters),
        "cities": get_cities_rows(db, filters),
        "seniority": get_seniority_rows(db, filters),
        "salaryRanges": get_salary_ranges(db, filters),
        "metadata": {
            "filtersApplied": serialize_filters(filters),
            "source": "database",
        },
    }


@router.get("/technologies")
def get_technologies(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
    limit: int = ApiQuery(default=30, ge=1, le=100),
):
    return get_technology_rows(db, filters, limit=limit)


@router.get("/cities")
def get_cities(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
):
    return get_cities_rows(db, filters)


@router.get("/seniority")
def get_seniority(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
):
    return get_seniority_rows(db, filters)


@router.get("/categories")
def get_categories(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
):
    return get_category_breakdown(db, filters)


@router.get("/data-quality")
def get_data_quality(
    filters: dict[str, Any] = Depends(build_filters),
    db: Session = Depends(get_db),
):
    total_jobs = count_filtered_jobs(db, filters)

    if total_jobs == 0:
        return {
            "summary": {
                "totalJobs": 0,
                "qualityScore": 0,
            },
            "issues": {},
            "metadata": {
                "filtersApplied": serialize_filters(filters),
                "source": "database",
            },
        }

    base_query = db.query(JobPosting)
    base_query = apply_job_filters(base_query, filters)

    missing_salary = base_query.filter(
        JobPosting.salary_min.is_(None),
        JobPosting.salary_max.is_(None),
    ).count()

    missing_published_at = base_query.filter(JobPosting.published_at.is_(None)).count()

    unknown_seniority = base_query.filter(
        JobPosting.seniority.in_(["unknown", None])
    ).count()

    unknown_modality = base_query.filter(
        JobPosting.modality.in_(["unknown", None])
    ).count()

    unknown_category = base_query.filter(
        JobPosting.category.in_(["unknown", "other", None])
    ).count()

    jobs_without_technologies_query = (
        db.query(func.count(JobPosting.id))
        .outerjoin(JobPostingTechnology, JobPostingTechnology.job_posting_id == JobPosting.id)
        .filter(JobPostingTechnology.id.is_(None))
    )
    jobs_without_technologies_query = apply_job_filters(jobs_without_technologies_query, filters)
    jobs_without_technologies = int(jobs_without_technologies_query.scalar() or 0)

    duplicate_urls_query = (
        db.query(
            JobPosting.source_url.label("source_url"),
            func.count(JobPosting.id).label("duplicate_count"),
        )
        .filter(JobPosting.source_url.isnot(None))
        .group_by(JobPosting.source_url)
        .having(func.count(JobPosting.id) > 1)
    )
    duplicate_urls_query = apply_job_filters(duplicate_urls_query, filters)

    duplicate_urls = [
        {
            "sourceUrl": row.source_url,
            "count": int(row.duplicate_count or 0),
        }
        for row in duplicate_urls_query.all()
    ]

    blocking_issues = (
        jobs_without_technologies
        + len(duplicate_urls)
    )

    soft_issues = (
        missing_salary
        + missing_published_at
        + unknown_seniority
        + unknown_modality
        + unknown_category
    )

    raw_score = 100 - round(((blocking_issues * 2) + soft_issues) / max(total_jobs, 1) * 10)
    quality_score = max(0, min(100, raw_score))

    return {
        "summary": {
            "totalJobs": total_jobs,
            "qualityScore": quality_score,
        },
        "issues": {
            "missingSalary": missing_salary,
            "missingPublishedAt": missing_published_at,
            "unknownSeniority": unknown_seniority,
            "unknownModality": unknown_modality,
            "unknownCategory": unknown_category,
            "jobsWithoutTechnologies": jobs_without_technologies,
            "duplicateUrls": duplicate_urls,
        },
        "metadata": {
            "filtersApplied": serialize_filters(filters),
            "source": "database",
        },
    }