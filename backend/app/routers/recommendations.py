from collections import defaultdict
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.database.models import JobPosting, JobPostingTechnology, Technology
from app.database.session import get_db


router = APIRouter(prefix="/api/v1", tags=["Recommendations"])


CAREER_PATHS = [
    {
        "title": "Frontend Engineer",
        "description": "Construye interfaces modernas para startups, fintechs y empresas SaaS.",
        "target_techs": [
            "React",
            "TypeScript",
            "JavaScript",
            "Next.js",
            "TailwindCSS",
            "HTML",
            "CSS",
            "Angular",
            "Vue",
        ],
        "fallback_categories": ["Frontend", "Language"],
        "timeWeeks": 16,
    },
    {
        "title": "Backend Engineer",
        "description": "Desarrolla APIs, servicios y lógica de negocio usando bases de datos y cloud.",
        "target_techs": [
            "Python",
            "FastAPI",
            "Django",
            "Node.js",
            "Express",
            "Java",
            "Spring Boot",
            "C#",
            "PostgreSQL",
            "SQL",
            "Docker",
        ],
        "fallback_categories": ["Backend", "Database", "Language", "DevOps"],
        "timeWeeks": 20,
    },
    {
        "title": "Data Analyst",
        "description": "Transforma datos en reportes, dashboards e insights para toma de decisiones.",
        "target_techs": [
            "SQL",
            "Python",
            "Power BI",
            "Excel",
            "Pandas",
            "PostgreSQL",
            "NumPy",
        ],
        "fallback_categories": ["Data", "Database", "Language"],
        "timeWeeks": 14,
    },
    {
        "title": "Cloud & DevOps",
        "description": "Automatiza infraestructura, despliegues y ambientes cloud.",
        "target_techs": [
            "AWS",
            "Docker",
            "Kubernetes",
            "Terraform",
            "CI/CD",
            "GitHub",
            "Azure",
            "GCP",
        ],
        "fallback_categories": ["Cloud", "DevOps"],
        "timeWeeks": 24,
    },
]


def salary_midpoint_expression():
    return (
        func.coalesce(JobPosting.salary_min, JobPosting.salary_max)
        + func.coalesce(JobPosting.salary_max, JobPosting.salary_min)
    ) / 2.0


def get_technology_metrics(db: Session) -> list[dict[str, Any]]:
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

    metrics = []

    for row in rows:
        demand = int(row.demand or 0)
        junior_count = int(row.junior_count or 0)
        junior_friendly = round((junior_count / demand) * 100) if demand else 0

        metrics.append(
            {
                "name": row.name,
                "category": row.category,
                "demand": demand,
                "trend": 0,
                "juniorFriendly": junior_friendly,
                "avgSalaryCLP": int(row.avg_salary or 0),
                "related": [],
            }
        )

    by_category: dict[str, list[str]] = defaultdict(list)

    for item in metrics:
        by_category[item["category"]].append(item["name"])

    for item in metrics:
        item["related"] = [
            name for name in by_category[item["category"]] if name != item["name"]
        ][:4]

    return metrics


def select_stack(
    path_config: dict[str, Any],
    technologies_by_name: dict[str, dict[str, Any]],
    all_technologies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []

    for tech_name in path_config["target_techs"]:
        technology = technologies_by_name.get(tech_name)

        if technology and technology["name"] not in [item["name"] for item in selected]:
            selected.append(technology)

        if len(selected) == 4:
            return selected

    fallback_categories = set(path_config["fallback_categories"])

    for technology in all_technologies:
        already_selected = technology["name"] in [item["name"] for item in selected]

        if technology["category"] in fallback_categories and not already_selected:
            selected.append(technology)

        if len(selected) == 4:
            break

    return selected


def weighted_average(items: list[dict[str, Any]], key: str) -> int:
    total_demand = sum(item["demand"] for item in items)

    if total_demand == 0:
        return 0

    return round(
        sum(item[key] * item["demand"] for item in items) / total_demand
    )


@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    all_technologies = get_technology_metrics(db)
    technologies_by_name = {technology["name"]: technology for technology in all_technologies}

    paths = []

    for path_config in CAREER_PATHS:
        stack = select_stack(path_config, technologies_by_name, all_technologies)

        total_demand = sum(technology["demand"] for technology in stack)
        junior_score = weighted_average(stack, "juniorFriendly")
        avg_salary = weighted_average(stack, "avgSalaryCLP")

        paths.append(
            {
                "title": path_config["title"],
                "description": path_config["description"],
                "techs": [technology["name"] for technology in stack],
                "demandScore": 0,
                "juniorScore": junior_score,
                "timeWeeks": path_config["timeWeeks"],
                "totalDemand": total_demand,
                "avgSalaryCLP": avg_salary,
            }
        )

    max_total_demand = max([path["totalDemand"] for path in paths], default=1)

    for path in paths:
        path["demandScore"] = round((path["totalDemand"] / max_total_demand) * 100)

    paths = sorted(paths, key=lambda path: path["demandScore"], reverse=True)

    suggested = sorted(
        all_technologies,
        key=lambda technology: technology["demand"] * (1 + technology["juniorFriendly"] / 100),
        reverse=True,
    )[:6]

    return {
        "learningPaths": paths,
        "suggested": suggested,
        "metadata": {
            "totalTechnologies": len(all_technologies),
            "totalPaths": len(paths),
            "source": "database",
        },
    }