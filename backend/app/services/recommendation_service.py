from typing import Any, Final, TypedDict

from sqlalchemy.orm import Session

from app.schemas.filters import StatsFilters
from app.services.stats_service import get_technology_rows


class CareerPathConfig(TypedDict):
    title: str
    description: str
    target_techs: tuple[str, ...]
    fallback_categories: tuple[str, ...]
    time_weeks: int


TechnologyMetric = dict[str, Any]


CAREER_PATHS: Final[tuple[CareerPathConfig, ...]] = (
    {
        "title": "Frontend Engineer",
        "description": ("Construye interfaces modernas para startups, fintechs y empresas SaaS."),
        "target_techs": (
            "React",
            "TypeScript",
            "JavaScript",
            "Next.js",
            "TailwindCSS",
            "HTML",
            "CSS",
            "Angular",
            "Vue",
        ),
        "fallback_categories": ("Frontend", "Language"),
        "time_weeks": 16,
    },
    {
        "title": "Backend Engineer",
        "description": (
            "Desarrolla APIs, servicios y lógica de negocio usando bases de datos y cloud."
        ),
        "target_techs": (
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
        ),
        "fallback_categories": (
            "Backend",
            "Database",
            "Language",
            "DevOps",
        ),
        "time_weeks": 20,
    },
    {
        "title": "Data Analyst",
        "description": (
            "Transforma datos en reportes, dashboards e insights para toma de decisiones."
        ),
        "target_techs": (
            "SQL",
            "Python",
            "Power BI",
            "Excel",
            "Pandas",
            "PostgreSQL",
            "NumPy",
        ),
        "fallback_categories": (
            "Data",
            "Database",
            "Language",
        ),
        "time_weeks": 14,
    },
    {
        "title": "Cloud & DevOps",
        "description": ("Automatiza infraestructura, despliegues y ambientes cloud."),
        "target_techs": (
            "AWS",
            "Docker",
            "Kubernetes",
            "Terraform",
            "CI/CD",
            "GitHub",
            "Azure",
            "GCP",
        ),
        "fallback_categories": ("Cloud", "DevOps"),
        "time_weeks": 24,
    },
)


def select_stack(
    path_config: CareerPathConfig,
    technologies_by_name: dict[str, TechnologyMetric],
    all_technologies: list[TechnologyMetric],
    stack_size: int = 4,
) -> list[TechnologyMetric]:
    selected: list[TechnologyMetric] = []
    selected_names: set[str] = set()

    for tech_name in path_config["target_techs"]:
        technology = technologies_by_name.get(tech_name)

        if technology is None or tech_name in selected_names:
            continue

        selected.append(technology)
        selected_names.add(tech_name)

        if len(selected) == stack_size:
            return selected

    fallback_categories = set(path_config["fallback_categories"])

    for technology in all_technologies:
        name = str(technology["name"])
        category = str(technology["category"])

        if name in selected_names or category not in fallback_categories:
            continue

        selected.append(technology)
        selected_names.add(name)

        if len(selected) == stack_size:
            break

    return selected


def weighted_average(
    items: list[TechnologyMetric],
    key: str,
) -> int:
    total_demand = sum(int(item["demand"]) for item in items)

    if total_demand == 0:
        return 0

    weighted_total = sum(int(item[key]) * int(item["demand"]) for item in items)

    return round(weighted_total / total_demand)


def build_recommendations(db: Session) -> dict[str, Any]:
    all_technologies = get_technology_rows(
        db,
        StatsFilters(),
        limit=None,
    )

    technologies_by_name = {str(technology["name"]): technology for technology in all_technologies}

    learning_paths: list[dict[str, Any]] = []

    for path_config in CAREER_PATHS:
        stack = select_stack(
            path_config,
            technologies_by_name,
            all_technologies,
        )

        total_demand = sum(int(technology["demand"]) for technology in stack)

        learning_paths.append(
            {
                "title": path_config["title"],
                "description": path_config["description"],
                "techs": [str(technology["name"]) for technology in stack],
                "demandScore": 0,
                "juniorScore": weighted_average(
                    stack,
                    "juniorFriendly",
                ),
                "timeWeeks": path_config["time_weeks"],
                "totalDemand": total_demand,
                "avgSalaryCLP": weighted_average(
                    stack,
                    "avgSalaryCLP",
                ),
            }
        )

    max_demand = max(
        (path["totalDemand"] for path in learning_paths),
        default=0,
    )

    if max_demand > 0:
        for path in learning_paths:
            path["demandScore"] = round(path["totalDemand"] / max_demand * 100)

    learning_paths.sort(
        key=lambda path: path["demandScore"],
        reverse=True,
    )

    suggested = sorted(
        all_technologies,
        key=lambda technology: (
            int(technology["demand"]) * (1 + int(technology["juniorFriendly"]) / 100)
        ),
        reverse=True,
    )[:6]

    return {
        "learningPaths": learning_paths,
        "suggested": suggested,
        "metadata": {
            "totalTechnologies": len(all_technologies),
            "totalPaths": len(learning_paths),
            "source": "database",
        },
    }
