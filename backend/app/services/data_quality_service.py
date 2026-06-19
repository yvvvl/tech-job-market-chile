from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import JobPosting, JobPostingTechnology
from app.schemas.filters import StatsFilters
from app.services.stats_service import apply_job_filters, count_filtered_jobs


def get_data_quality(db: Session, filters: StatsFilters) -> dict:
    total_jobs = count_filtered_jobs(db, filters)

    if total_jobs == 0:
        return {
            "summary": {
                "totalJobs": 0,
                "qualityScore": 0,
            },
            "issues": {},
            "metadata": {
                "filtersApplied": filters.serialized(),
                "source": "database",
            },
        }

    base_query = db.query(JobPosting)
    base_query = apply_job_filters(base_query, filters)

    missing_salary = base_query.filter(
        JobPosting.salary_min.is_(None),
        JobPosting.salary_max.is_(None),
    ).count()

    missing_published_at = base_query.filter(JobPosting.published_at.is_(None)).count()

    unknown_seniority = base_query.filter(JobPosting.seniority.in_(["unknown", None])).count()
    unknown_modality = base_query.filter(JobPosting.modality.in_(["unknown", None])).count()
    unknown_category = base_query.filter(
        JobPosting.category.in_(["unknown", "other", None])
    ).count()

    jobs_without_technologies_query = (
        db.query(func.count(JobPosting.id))
        .outerjoin(
            JobPostingTechnology,
            JobPostingTechnology.job_posting_id == JobPosting.id,
        )
        .filter(JobPostingTechnology.id.is_(None))
    )
    jobs_without_technologies_query = apply_job_filters(jobs_without_technologies_query, filters)
    jobs_without_technologies = int(jobs_without_technologies_query.scalar() or 0)

    duplicate_urls_query = (
        db.query(
            JobPosting.source_url.label("source_url"),
            func.count(JobPosting.id).label("duplicate_count"),
        )
        .filter(JobPosting.source_url.isnot(None))
        .group_by(JobPosting.source_url)
        .having(func.count(JobPosting.id) > 1)
    )
    duplicate_urls_query = apply_job_filters(duplicate_urls_query, filters)

    duplicate_urls = [
        {
            "sourceUrl": row.source_url,
            "count": int(row.duplicate_count or 0),
        }
        for row in duplicate_urls_query.all()
    ]

    blocking_issues = jobs_without_technologies + len(duplicate_urls)

    soft_issues = (
        missing_salary
        + missing_published_at
        + unknown_seniority
        + unknown_modality
        + unknown_category
    )

    raw_score = 100 - round(((blocking_issues * 2) + soft_issues) / max(total_jobs, 1) * 10)
    quality_score = max(0, min(100, raw_score))

    return {
        "summary": {
            "totalJobs": total_jobs,
            "qualityScore": quality_score,
        },
        "issues": {
            "missingSalary": missing_salary,
            "missingPublishedAt": missing_published_at,
            "unknownSeniority": unknown_seniority,
            "unknownModality": unknown_modality,
            "unknownCategory": unknown_category,
            "jobsWithoutTechnologies": jobs_without_technologies,
            "duplicateUrls": duplicate_urls,
        },
        "metadata": {
            "filtersApplied": filters.serialized(),
            "source": "database",
        },
    }
