from app.schemas.recommendations import RecommendationsResponse
from app.schemas.stats import DataQualityResponse, OverviewResponse


def test_overview_schema_preserves_camel_case_contract() -> None:
    payload = {
        "stats": {
            "totalJobs": 3,
            "companies": 2,
            "technologies": 4,
            "cities": 2,
        },
        "monthlyTrend": [
            {
                "month": "Jun",
                "jobs": 3,
                "junior": 2,
            }
        ],
        "technologies": [
            {
                "name": "Python",
                "category": "Language",
                "demand": 2,
                "trend": 0,
                "juniorFriendly": 100,
                "avgSalaryCLP": 1_200_000,
                "related": ["FastAPI"],
            }
        ],
        "categoryBreakdown": [
            {
                "category": "backend",
                "demand": 2,
            }
        ],
        "cities": [
            {
                "city": "Santiago",
                "jobs": 2,
            }
        ],
        "seniority": [
            {
                "level": "Junior",
                "count": 2,
                "fill": "var(--color-chart-2)",
            }
        ],
        "salaryRanges": [
            {
                "range": "1M – 1.5M",
                "count": 2,
            }
        ],
        "metadata": {
            "filtersApplied": {},
            "source": "database",
        },
    }

    model = OverviewResponse.model_validate(payload)
    serialized = model.model_dump(by_alias=True)

    assert serialized["stats"]["totalJobs"] == 3
    assert serialized["monthlyTrend"][0]["junior"] == 2
    assert serialized["technologies"][0]["juniorFriendly"] == 100
    assert serialized["categoryBreakdown"][0]["category"] == "backend"


def test_data_quality_schema_fills_empty_issues() -> None:
    payload = {
        "summary": {
            "totalJobs": 0,
            "qualityScore": 0,
        },
        "issues": {},
        "metadata": {
            "filtersApplied": {},
            "source": "database",
        },
    }

    model = DataQualityResponse.model_validate(payload)
    serialized = model.model_dump(by_alias=True)

    assert serialized["issues"]["missingSalary"] == 0
    assert serialized["issues"]["duplicateUrls"] == []


def test_recommendations_schema_preserves_contract() -> None:
    payload = {
        "learningPaths": [
            {
                "title": "Backend Engineer",
                "description": "Backend path",
                "techs": ["Python", "FastAPI"],
                "demandScore": 100,
                "juniorScore": 75,
                "timeWeeks": 20,
                "totalDemand": 10,
                "avgSalaryCLP": 1_500_000,
            }
        ],
        "suggested": [
            {
                "name": "Python",
                "category": "Language",
                "demand": 5,
                "trend": 0,
                "juniorFriendly": 80,
                "avgSalaryCLP": 1_400_000,
                "related": [],
            }
        ],
        "metadata": {
            "totalTechnologies": 1,
            "totalPaths": 1,
            "source": "database",
        },
    }

    model = RecommendationsResponse.model_validate(payload)
    serialized = model.model_dump(by_alias=True)

    assert serialized["learningPaths"][0]["demandScore"] == 100
    assert serialized["metadata"]["totalTechnologies"] == 1
