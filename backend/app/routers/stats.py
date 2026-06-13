from collections import defaultdict

from fastapi import APIRouter, Depends
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
    "unknown": "Unknown",
}

SENIORITY_COLORS = {
    "trainee": "var(--color-chart-2)",
    "junior": "var(--color-chart-2)",
    "semi_senior": "var(--color-chart-1)",
    "senior": "var(--color-chart-3)",
    "unknown": "var(--color-chart-4)",
}


def salary_midpoint_expression():
    return (
        func.coalesce(JobPosting.salary_min, JobPosting.salary_max)
        + func.coalesce(JobPosting.salary_max, JobPosting.salary_min)
    ) / 2.0


def get_technology_rows(db: Session) -> list[dict]:
    salary_mid = salary_midpoint_expression()

    junior_case = case(
        (JobPosting.seniority.in_(["trainee", "junior"]), 1),
        else_=0,
    )

    rows = (
        db.query(
            Technology.name.label("name"),
            Technology.category.label("category"),
            func.count(JobPostingTechnology.job_posting_id).label("demand"),
            func.sum(junior_case).label("junior_count"),
            func.avg(salary_mid).label("avg_salary"),
        )
        .join(JobPostingTechnology, JobPostingTechnology.technology_id == Technology.id)
        .join(JobPosting, JobPosting.id == JobPostingTechnology.job_posting_id)
        .group_by(Technology.id, Technology.name, Technology.category)
        .order_by(func.count(JobPostingTechnology.job_posting_id).desc())
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


def get_cities_rows(db: Session) -> list[dict]:
    rows = (
        db.query(JobPosting.city, func.count(JobPosting.id).label("jobs"))
        .group_by(JobPosting.city)
        .order_by(func.count(JobPosting.id).desc())
        .all()
    )

    return [
        {"city": row.city or "Unknown", "jobs": int(row.jobs or 0)}
        for row in rows
    ]


def get_seniority_rows(db: Session) -> list[dict]:
    rows = (
        db.query(
            JobPosting.seniority.label("seniority"),
            func.count(JobPosting.id).label("job_count"),
        )
        .group_by(JobPosting.seniority)
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

def get_salary_ranges(db: Session) -> list[dict]:
    salaries = []
    postings = db.query(JobPosting.salary_min, JobPosting.salary_max).all()

    for posting in postings:
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


def get_monthly_trend(db: Session) -> list[dict]:
    month_expr = func.date_trunc("month", JobPosting.published_at)

    junior_case = case(
        (JobPosting.seniority.in_(["trainee", "junior"]), 1),
        else_=0,
    )

    rows = (
        db.query(
            func.to_char(month_expr, "Mon").label("month"),
            func.count(JobPosting.id).label("jobs"),
            func.sum(junior_case).label("junior"),
            month_expr.label("month_date"),
        )
        .filter(JobPosting.published_at.isnot(None))
        .group_by(month_expr)
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


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    technologies = get_technology_rows(db)
    cities = get_cities_rows(db)
    seniority = get_seniority_rows(db)
    monthly_trend = get_monthly_trend(db)
    salary_ranges = get_salary_ranges(db)

    category_map: dict[str, int] = defaultdict(int)

    for tech in technologies:
        category_map[tech["category"]] += tech["demand"]

    category_breakdown = [
        {"category": category, "demand": demand}
        for category, demand in sorted(category_map.items(), key=lambda item: item[1], reverse=True)
    ]

    stats = {
        "totalJobs": int(db.query(func.count(JobPosting.id)).scalar() or 0),
        "companies": int(db.query(func.count(Company.id)).scalar() or 0),
        "technologies": int(db.query(func.count(Technology.id)).scalar() or 0),
        "cities": int(db.query(func.count(func.distinct(JobPosting.city))).scalar() or 0),
    }

    return {
        "stats": stats,
        "monthlyTrend": monthly_trend,
        "technologies": technologies,
        "categoryBreakdown": category_breakdown,
        "cities": cities,
        "seniority": seniority,
        "salaryRanges": salary_ranges,
    }


@router.get("/technologies")
def get_technologies(db: Session = Depends(get_db)):
    return get_technology_rows(db)


@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    return get_cities_rows(db)


@router.get("/seniority")
def get_seniority(db: Session = Depends(get_db)):
    return get_seniority_rows(db)