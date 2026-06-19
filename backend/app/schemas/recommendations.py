from typing import Literal

from pydantic import Field

from app.schemas.common import ApiSchema
from app.schemas.stats import TechnologyResponse


class LearningPathResponse(ApiSchema):
    title: str
    description: str
    techs: list[str]
    demand_score: int = Field(
        alias="demandScore",
        ge=0,
        le=100,
    )
    junior_score: int = Field(
        alias="juniorScore",
        ge=0,
        le=100,
    )
    time_weeks: int = Field(
        alias="timeWeeks",
        ge=0,
    )
    total_demand: int = Field(
        alias="totalDemand",
        ge=0,
    )
    avg_salary_clp: int = Field(
        alias="avgSalaryCLP",
        ge=0,
    )


class RecommendationsMetadata(ApiSchema):
    total_technologies: int = Field(
        alias="totalTechnologies",
        ge=0,
    )
    total_paths: int = Field(
        alias="totalPaths",
        ge=0,
    )
    source: Literal["database"] = "database"


class RecommendationsResponse(ApiSchema):
    learning_paths: list[LearningPathResponse] = Field(
        alias="learningPaths",
    )
    suggested: list[TechnologyResponse]
    metadata: RecommendationsMetadata
