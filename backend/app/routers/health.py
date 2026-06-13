from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Company, JobPosting, Technology
from app.database.session import check_database_connection, get_db


router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_connected = check_database_connection()

    return {
        "status": "ok" if db_connected else "error",
        "api": "running",
        "database": "connected" if db_connected else "disconnected",
        "total_jobs": db.query(func.count(JobPosting.id)).scalar() if db_connected else 0,
        "companies": db.query(func.count(Company.id)).scalar() if db_connected else 0,
        "technologies": db.query(func.count(Technology.id)).scalar() if db_connected else 0,
    }