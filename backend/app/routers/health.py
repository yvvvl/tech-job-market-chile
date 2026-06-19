from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Company, JobPosting, Technology
from app.database.session import check_database_connection, get_db
from app.schemas.health import HealthResponse

router = APIRouter(
    prefix="/api/v1",
    tags=["Health"],
)


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check(
    db: Session = Depends(get_db),
) -> HealthResponse:
    db_connected = check_database_connection()

    total_jobs = int(db.query(func.count(JobPosting.id)).scalar() or 0) if db_connected else 0

    companies = int(db.query(func.count(Company.id)).scalar() or 0) if db_connected else 0

    technologies = int(db.query(func.count(Technology.id)).scalar() or 0) if db_connected else 0

    return HealthResponse(
        status="ok" if db_connected else "error",
        api="running",
        database="connected" if db_connected else "disconnected",
        total_jobs=total_jobs,
        companies=companies,
        technologies=technologies,
    )
