from typing import Any

from fastapi import APIRouter, Depends
from fastapi import Query as ApiQuery
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.filters import StatsFilters, build_filters
from app.services.data_quality_service import get_data_quality
from app.services.stats_service import (
    get_category_breakdown,
    get_cities_rows,
    get_overview,
    get_seniority_rows,
    get_technology_rows,
)

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])


@router.get("/overview")
def overview(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return get_overview(db, filters)


@router.get("/technologies")
def technologies(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
    limit: int = ApiQuery(default=30, ge=1, le=100),
) -> list[dict]:
    return get_technology_rows(db, filters, limit=limit)


@router.get("/cities")
def cities(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> list[dict]:
    return get_cities_rows(db, filters)


@router.get("/seniority")
def seniority(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> list[dict]:
    return get_seniority_rows(db, filters)


@router.get("/categories")
def categories(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> list[dict]:
    return get_category_breakdown(db, filters)


@router.get("/data-quality")
def data_quality(
    filters: StatsFilters = Depends(build_filters),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return get_data_quality(db, filters)
