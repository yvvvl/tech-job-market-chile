from pydantic import Field

from app.schemas.common import ApiSchema, ResponseMetadata


class StatsSummary(ApiSchema):
    total_jobs: int = Field(alias="totalJobs", ge=0)
    companies: int = Field(ge=0)
    technologies: int = Field(ge=0)
    cities: int = Field(ge=0)


class MonthlyTrendResponse(ApiSchema):
    month: str
    jobs: int = Field(ge=0)
    junior: int = Field(ge=0)


class TechnologyResponse(ApiSchema):
    name: str
    category: str
    demand: int = Field(ge=0)
    trend: int
    junior_friendly: int = Field(
        alias="juniorFriendly",
        ge=0,
        le=100,
    )
    avg_salary_clp: int = Field(
        alias="avgSalaryCLP",
        ge=0,
    )
    related: list[str] = Field(default_factory=list)


class CategoryResponse(ApiSchema):
    category: str
    demand: int = Field(ge=0)


class CityResponse(ApiSchema):
    city: str
    jobs: int = Field(ge=0)


class SeniorityResponse(ApiSchema):
    level: str
    count: int = Field(ge=0)
    fill: str


class SalaryRangeResponse(ApiSchema):
    range: str
    count: int = Field(ge=0)


class OverviewResponse(ApiSchema):
    stats: StatsSummary
    monthly_trend: list[MonthlyTrendResponse] = Field(
        alias="monthlyTrend",
    )
    technologies: list[TechnologyResponse]
    category_breakdown: list[CategoryResponse] = Field(
        alias="categoryBreakdown",
    )
    cities: list[CityResponse]
    seniority: list[SeniorityResponse]
    salary_ranges: list[SalaryRangeResponse] = Field(
        alias="salaryRanges",
    )
    metadata: ResponseMetadata


class DuplicateUrlResponse(ApiSchema):
    source_url: str = Field(alias="sourceUrl")
    count: int = Field(ge=2)


class DataQualitySummary(ApiSchema):
    total_jobs: int = Field(alias="totalJobs", ge=0)
    quality_score: int = Field(
        alias="qualityScore",
        ge=0,
        le=100,
    )


class DataQualityIssues(ApiSchema):
    missing_salary: int = Field(
        default=0,
        alias="missingSalary",
        ge=0,
    )
    missing_published_at: int = Field(
        default=0,
        alias="missingPublishedAt",
        ge=0,
    )
    unknown_seniority: int = Field(
        default=0,
        alias="unknownSeniority",
        ge=0,
    )
    unknown_modality: int = Field(
        default=0,
        alias="unknownModality",
        ge=0,
    )
    unknown_category: int = Field(
        default=0,
        alias="unknownCategory",
        ge=0,
    )
    jobs_without_technologies: int = Field(
        default=0,
        alias="jobsWithoutTechnologies",
        ge=0,
    )
    duplicate_urls: list[DuplicateUrlResponse] = Field(
        default_factory=list,
        alias="duplicateUrls",
    )


class DataQualityResponse(ApiSchema):
    summary: DataQualitySummary
    issues: DataQualityIssues = Field(
        default_factory=DataQualityIssues,
    )
    metadata: ResponseMetadata
