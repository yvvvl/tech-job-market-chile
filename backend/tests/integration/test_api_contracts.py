import pytest
from fastapi.testclient import TestClient


pytestmark = pytest.mark.integration


def test_root_contract(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["docs"] == "/docs"
    assert data["health"] == "/api/v1/health"
    assert data["overview"] == "/api/v1/stats/overview"


def test_health_contract(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["api"] == "running"
    assert data["database"] == "connected"
    assert isinstance(data["total_jobs"], int)
    assert isinstance(data["companies"], int)
    assert isinstance(data["technologies"], int)
    assert data["total_jobs"] > 0


def test_overview_contract(client: TestClient) -> None:
    response = client.get("/api/v1/stats/overview")

    assert response.status_code == 200

    data = response.json()

    assert {
        "stats",
        "monthlyTrend",
        "technologies",
        "categoryBreakdown",
        "cities",
        "seniority",
        "salaryRanges",
        "metadata",
    }.issubset(data)

    assert {
        "totalJobs",
        "companies",
        "technologies",
        "cities",
    }.issubset(data["stats"])

    assert isinstance(data["monthlyTrend"], list)
    assert isinstance(data["technologies"], list)
    assert isinstance(data["categoryBreakdown"], list)
    assert isinstance(data["cities"], list)
    assert isinstance(data["seniority"], list)
    assert isinstance(data["salaryRanges"], list)


def test_overview_filters_contract(client: TestClient) -> None:
    response = client.get(
        "/api/v1/stats/overview",
        params={
            "seniority": "junior",
            "modality": "remoto",
        },
    )

    assert response.status_code == 200

    data = response.json()
    applied = data["metadata"]["filtersApplied"]

    assert applied["seniority"] == "junior"
    assert applied["modality"] == "remoto"


def test_technologies_contract(client: TestClient) -> None:
    response = client.get(
        "/api/v1/stats/technologies",
        params={"limit": 10},
    )

    assert response.status_code == 200

    technologies = response.json()

    assert isinstance(technologies, list)
    assert len(technologies) <= 10

    if technologies:
        assert {
            "name",
            "category",
            "demand",
            "trend",
            "juniorFriendly",
            "avgSalaryCLP",
            "related",
        }.issubset(technologies[0])


def test_categories_contract(client: TestClient) -> None:
    response = client.get("/api/v1/stats/categories")

    assert response.status_code == 200

    categories = response.json()

    assert isinstance(categories, list)

    if categories:
        assert {"category", "demand"}.issubset(categories[0])


def test_data_quality_contract(client: TestClient) -> None:
    response = client.get("/api/v1/stats/data-quality")

    assert response.status_code == 200

    data = response.json()

    assert {"summary", "issues", "metadata"}.issubset(data)
    assert {"totalJobs", "qualityScore"}.issubset(data["summary"])

    quality_score = data["summary"]["qualityScore"]

    assert isinstance(quality_score, int)
    assert 0 <= quality_score <= 100


def test_recommendations_contract(client: TestClient) -> None:
    response = client.get("/api/v1/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert {
        "learningPaths",
        "suggested",
        "metadata",
    }.issubset(data)

    assert isinstance(data["learningPaths"], list)
    assert isinstance(data["suggested"], list)

    if data["learningPaths"]:
        assert {
            "title",
            "description",
            "techs",
            "demandScore",
            "juniorScore",
            "timeWeeks",
            "totalDemand",
            "avgSalaryCLP",
        }.issubset(data["learningPaths"][0])