from app.services.recommendation_service import (
    CareerPathConfig,
    select_stack,
    weighted_average,
)


def technology(
    name: str,
    category: str,
    demand: int,
    junior_friendly: int,
    salary: int,
) -> dict:
    return {
        "name": name,
        "category": category,
        "demand": demand,
        "trend": 0,
        "juniorFriendly": junior_friendly,
        "avgSalaryCLP": salary,
        "related": [],
    }


def test_weighted_average_uses_demand_as_weight() -> None:
    items = [
        technology("Python", "Language", 10, 80, 1_000_000),
        technology("Java", "Language", 30, 40, 2_000_000),
    ]

    assert weighted_average(items, "juniorFriendly") == 50
    assert weighted_average(items, "avgSalaryCLP") == 1_750_000


def test_weighted_average_returns_zero_for_empty_stack() -> None:
    assert weighted_average([], "juniorFriendly") == 0


def test_select_stack_prioritizes_target_technologies() -> None:
    technologies = [
        technology("Python", "Language", 10, 70, 1_500_000),
        technology("FastAPI", "Backend", 5, 60, 1_600_000),
        technology("PostgreSQL", "Database", 8, 50, 1_700_000),
        technology("Docker", "DevOps", 6, 40, 1_800_000),
        technology("Java", "Language", 20, 30, 2_000_000),
    ]

    config: CareerPathConfig = {
        "title": "Backend",
        "description": "Backend path",
        "target_techs": (
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ),
        "fallback_categories": (
            "Backend",
            "Database",
            "Language",
            "DevOps",
        ),
        "time_weeks": 20,
    }

    by_name = {item["name"]: item for item in technologies}

    stack = select_stack(
        config,
        by_name,
        technologies,
    )

    assert [item["name"] for item in stack] == [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
    ]


def test_select_stack_uses_category_fallbacks() -> None:
    technologies = [
        technology("Java", "Language", 20, 30, 2_000_000),
        technology("Docker", "DevOps", 10, 40, 1_800_000),
    ]

    config: CareerPathConfig = {
        "title": "Backend",
        "description": "Backend path",
        "target_techs": ("Python",),
        "fallback_categories": ("Language", "DevOps"),
        "time_weeks": 20,
    }

    stack = select_stack(
        config,
        {},
        technologies,
    )

    assert [item["name"] for item in stack] == [
        "Java",
        "Docker",
    ]
