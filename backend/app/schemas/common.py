from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ApiSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
        extra="forbid",
    )


class RootResponse(ApiSchema):
    message: str
    docs: str
    health: str
    overview: str


class ResponseMetadata(ApiSchema):
    filters_applied: dict[str, str] = Field(
        default_factory=dict,
        alias="filtersApplied",
    )
    source: Literal["database"] = "database"
