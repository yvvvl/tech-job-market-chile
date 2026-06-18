from collections import defaultdict

from sqlalchemy import case, func
from sqlalchemy.orm import Query, Session

from app.database.models import JobPosting, JobPostingTechnology, Technology
from app.schemas.filters import StatsFilters

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


def apply_job_filters(query: Query, filters: StatsFilters) -> Query:
    if filters.normalized_seniority:
        query = query.filter(JobPosting.seniority == filters.normalized_seniority)

    if filters.normalized_category:
        query = query.filter(JobPosting.category == filters.normalized_category)

    if filters.normalized_modality:
        query = query.filter(JobPosting.modality == filters.normalized_modality)

    if filters.city:
        query = query.filter(func.lower(JobPosting.city) == filters.city.strip().lower())

    if filters.source:
        query = query.filter(func.lower(JobPosting.source) == filters.source.strip().lower())

    date_expr = func.coalesce(JobPosting.published_at, JobPosting.collected_at)

    if filters.from_date:
        query = query.filter(date_expr >= filters.from_date)

    if filters.to_date:
        query = query.filter(date_expr <= filters.to_date)

    return query


def salary_midpoint_expression():
    return (
        func.coalesce(JobPosting.salary_min, JobPosting.salary_max)
        + func.coalesce(JobPosting.salary_max, JobPosting.salary_min)
    ) / 2.0


def count_filtered_jobs(db: Session, filters: StatsFilters) -> int:
    query = db.query(func.count(JobPosting.id))
    query = apply_job_filters(query, filters)

    return int(query.scalar() or 0)


def get_stats_summary(db: Session, filters: StatsFilters) -> dict:
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


def get_technology_rows(db: Session, filters: StatsFilters, limit: int = 30) -> list[dict]:
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

    technologies = []

    for row in rows:
        demand = int(row.demand or 0)
        junior_count = int(row.junior_count or 0)
        junior_friendly = round((junior_count / demand) * 100) if demand else 0
        avg_salary = int(row.avg_salary or 0)

        technologies.append(
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

    return add_related_technologies(technologies)


def add_related_technologies(technologies: list[dict]) -> list[dict]:
    by_category: dict[str, list[str]] = defaultdict(list)

    for item in technologies:
        by_category[item["category"]].append(item["name"])

    for item in technologies:
        item["related"] = [name for name in by_category[item["category"]] if name != item["name"]][
            :4
        ]

    return technologies


def get_cities_rows(db: Session, filters: StatsFilters) -> list[dict]:
    query = db.query(
        JobPosting.city.label("city"),
        func.count(JobPosting.id).label("job_count"),
    )

    query = apply_job_filters(query, filters)

    rows = query.group_by(JobPosting.city).order_by(func.count(JobPosting.id).desc()).all()

    return [
        {
            "city": row.city or "Unknown",
            "jobs": int(row.job_count or 0),
        }
        for row in rows
    ]


def get_seniority_rows(db: Session, filters: StatsFilters) -> list[dict]:
    query = db.query(
        JobPosting.seniority.label("seniority"),
        func.count(JobPosting.id).label("job_count"),
    )

    query = apply_job_filters(query, filters)

    rows = query.group_by(JobPosting.seniority).order_by(func.count(JobPosting.id).desc()).all()

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


def get_category_breakdown(db: Session, filters: StatsFilters) -> list[dict]:
    query = db.query(
        JobPosting.category.label("category"),
        func.count(JobPosting.id).label("demand"),
    )

    query = apply_job_filters(query, filters)

    rows = query.group_by(JobPosting.category).order_by(func.count(JobPosting.id).desc()).all()

    return [
        {
            "category": row.category or "unknown",
            "demand": int(row.demand or 0),
        }
        for row in rows
    ]


def get_salary_ranges(db: Session, filters: StatsFilters) -> list[dict]:
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


def get_monthly_trend(db: Session, filters: StatsFilters) -> list[dict]:
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

    rows = query.group_by(month_expr).order_by(month_expr).all()

    return [
        {
            "month": row.month.strip(),
            "jobs": int(row.jobs or 0),
            "junior": int(row.junior or 0),
        }
        for row in rows
    ]


def get_overview(db: Session, filters: StatsFilters) -> dict:
    return {
        "stats": get_stats_summary(db, filters),
        "monthlyTrend": get_monthly_trend(db, filters),
        "technologies": get_technology_rows(db, filters, limit=30),
        "categoryBreakdown": get_category_breakdown(db, filters),
        "cities": get_cities_rows(db, filters),
        "seniority": get_seniority_rows(db, filters),
        "salaryRanges": get_salary_ranges(db, filters),
        "metadata": {
            "filtersApplied": filters.serialized(),
            "source": "database",
        },
    }
