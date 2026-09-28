from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    jd_text = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=True)  # Extracted/provided list of required skills
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    creator = relationship("User", back_populates="job_descriptions")
    analysis_reports = relationship("AnalysisReport", back_populates="job_description", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<JobDescription id={self.id} title='{self.title}'>"
