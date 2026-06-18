from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    job_postings = relationship("JobPosting", back_populates="company")


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), unique=True, nullable=False, index=True)
    category = Column(String(80), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    job_postings = relationship("JobPostingTechnology", back_populates="technology")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(260), nullable=False, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)

    source = Column(String(80), nullable=False, default="manual", index=True)
    source_url = Column(String(800), nullable=True, index=True)

    city = Column(String(120), nullable=True, index=True)
    region = Column(String(120), nullable=True, index=True)
    modality = Column(String(50), nullable=True, index=True)
    seniority = Column(String(50), nullable=True, index=True)
    category = Column(String(50), nullable=True, index=True)

    description = Column(Text, nullable=True)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(20), nullable=True)

    published_at = Column(Date, nullable=True, index=True)
    collected_at = Column(Date, nullable=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    company = relationship("Company", back_populates="job_postings")
    technologies = relationship(
        "JobPostingTechnology",
        back_populates="job_posting",
        cascade="all, delete-orphan",
    )


class JobPostingTechnology(Base):
    __tablename__ = "job_posting_technologies"
    __table_args__ = (
        UniqueConstraint("job_posting_id", "technology_id", name="uq_job_technology"),
    )

    id = Column(Integer, primary_key=True, index=True)

    job_posting_id = Column(
        Integer,
        ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    technology_id = Column(
        Integer,
        ForeignKey("technologies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_posting = relationship("JobPosting", back_populates="technologies")
    technology = relationship("Technology", back_populates="job_postings")