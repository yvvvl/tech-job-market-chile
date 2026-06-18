from dataclasses import dataclass
from datetime import date
from typing import Any

from fastapi import Query as ApiQuery

from app.utils.normalization import normalize_slug


@dataclass(frozen=True)
class StatsFilters:
    seniority: str | None = None
    category: str | None = None
    city: str | None = None
    modality: str | None = None
    source: str | None = None
    from_date: date | None = None
    to_date: date | None = None

    def serialized(self) -> dict[str, str]:
        values: dict[str, Any] = {
            "seniority": self.seniority,
            "category": self.category,
            "city": self.city,
            "modality": self.modality,
            "source": self.source,
            "from_date": self.from_date,
            "to_date": self.to_date,
        }

        result: dict[str, str] = {}

        for key, value in values.items():
            if value is None:
                continue

            if isinstance(value, date):
                result[key] = value.isoformat()
            else:
                result[key] = str(value)

        return result

    @property
    def normalized_seniority(self) -> str | None:
        return normalize_slug(self.seniority)

    @property
    def normalized_category(self) -> str | None:
        return normalize_slug(self.category)

    @property
    def normalized_modality(self) -> str | None:
        return normalize_slug(self.modality)


def build_filters(
    seniority: str | None = ApiQuery(
        default=None,
        description="Ej: junior, trainee, senior",
    ),
    category: str | None = ApiQuery(
        default=None,
        description="Ej: backend, frontend, data",
    ),
    city: str | None = ApiQuery(
        default=None,
        description="Ej: Santiago, Remote, Concepción",
    ),
    modality: str | None = ApiQuery(
        default=None,
        description="Ej: remoto, hibrido, presencial",
    ),
    source: str | None = ApiQuery(
        default=None,
        description="Ej: LinkedIn, GetOnBoard, Laborum",
    ),
    from_date: date | None = ApiQuery(
        default=None,
        description="Fecha inicial YYYY-MM-DD",
    ),
    to_date: date | None = ApiQuery(
        default=None,
        description="Fecha final YYYY-MM-DD",
    ),
) -> StatsFilters:
    return StatsFilters(
        seniority=seniority,
        category=category,
        city=city,
        modality=modality,
        source=source,
        from_date=from_date,
        to_date=to_date,
    )
