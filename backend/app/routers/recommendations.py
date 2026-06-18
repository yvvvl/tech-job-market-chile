from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.recommendation_service import build_recommendations

router = APIRouter(
    prefix="/api/v1",
    tags=["Recommendations"],
)


@router.get("/recommendations")
def recommendations(
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return build_recommendations(db)
