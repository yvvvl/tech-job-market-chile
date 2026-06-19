from typing import Literal

from pydantic import Field

from app.schemas.common import ApiSchema


class HealthResponse(ApiSchema):
    status: Literal["ok", "error"]
    api: Literal["running"]
    database: Literal["connected", "disconnected"]
    total_jobs: int = Field(ge=0)
    companies: int = Field(ge=0)
    technologies: int = Field(ge=0)
