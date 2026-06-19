from typing import Any

from fastapi import APIRouter, Depends
from fastapi import Query as ApiQuery
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.filters import StatsFilters, build_filters
from app.schemas.stats import (
    CategoryResponse,
    CityResponse,
    DataQualityResponse,
    OverviewResponse,
    SeniorityResponse,
    TechnologyResponse,
)
from app.services.data_quality_service import get_data_quality
from app.services.stats_service import (
    get_category_breakdown,
    get_cities_rows,
    get_overview,
    get_seniority_rows,
    get_technology_rows,
)

router = APIRouter(
    prefix="/api/v1/stats",
    tags=["Stats"],
)


@router.get(
    "/overview",
    response_model=OverviewResponse,
)
def overview(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> Any:
    return get_overview(db, filters)


@router.get(
    "/technologies",
    response_model=list[TechnologyResponse],
)
def technologies(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
    limit: int = ApiQuery(default=30, ge=1, le=100),
) -> Any:
    return get_technology_rows(
        db,
        filters,
        limit=limit,
    )


@router.get(
    "/cities",
    response_model=list[CityResponse],
)
def cities(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> Any:
    return get_cities_rows(db, filters)


@router.get(
    "/seniority",
    response_model=list[SeniorityResponse],
)
def seniority(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> Any:
    return get_seniority_rows(db, filters)


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
)
def categories(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> Any:
    return get_category_breakdown(db, filters)


@router.get(
    "/data-quality",
    response_model=DataQualityResponse,
)
def data_quality(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> Any:
    return get_data_quality(db, filters)
