from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    ats_score = Column(Float, nullable=False, index=True)
    match_percentage = Column(Float, nullable=False, index=True)
    report_json = Column(JSON, nullable=False)  # Full comprehensive multi-agent breakdown
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="analysis_reports")
    job_description = relationship("JobDescription", back_populates="analysis_reports")

    def __repr__(self) -> str:
        return f"<AnalysisReport id={self.id} resume_id={self.resume_id} jd_id={self.jd_id} ats={self.ats_score}>"
