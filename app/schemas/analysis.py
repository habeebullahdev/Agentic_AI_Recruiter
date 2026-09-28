from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
    match_percentage: float = Field(..., ge=0, le=100, description="Overall skill match percentage")
    matched_skills: List[str] = Field(default_factory=list, description="Skills present in both resume and JD")
    missing_skills: List[str] = Field(default_factory=list, description="Required JD skills missing from resume")
    strong_skills: List[str] = Field(default_factory=list, description="Key high-value skills candidate excels at")
    analysis_notes: Optional[str] = Field(None, description="Detailed skill alignment insights")


class ATSComponentScore(BaseModel):
    score: float = Field(..., ge=0, le=100, description="Component score out of 100")
    weight: float = Field(..., description="Weight percentage in total ATS calculation")
    weighted_score: float = Field(..., description="Calculated contribution to total ATS score")
    reasoning: str = Field(..., description="Justification for component score")


class ATSScoreBreakdown(BaseModel):
    ats_score: float = Field(..., ge=0, le=100, description="Overall weighted ATS score (0-100)")
    skill_match: ATSComponentScore = Field(..., description="Skill match component (50% weight)")
    projects: ATSComponentScore = Field(..., description="Projects relevance component (20% weight)")
    experience: ATSComponentScore = Field(..., description="Experience alignment component (20% weight)")
    education: ATSComponentScore = Field(..., description="Education background component (10% weight)")
    overall_summary: str = Field(..., description="High level ATS screening verdict")


class InterviewQuestionsResult(BaseModel):
    technical_questions: List[str] = Field(default_factory=list, description="In-depth technical competency questions")
    project_questions: List[str] = Field(default_factory=list, description="Questions probing candidate's specific projects")
    behavioral_questions: List[str] = Field(default_factory=list, description="Scenario-based behavioral questions")
    hr_questions: List[str] = Field(default_factory=list, description="HR, cultural fit, and logistics questions")


class ResumeImprovementResult(BaseModel):
    missing_skills_suggestions: List[str] = Field(default_factory=list, description="Recommendations for acquiring missing skills")
    resume_enhancement_suggestions: List[str] = Field(default_factory=list, description="Bullet point phrasing and formatting improvements")
    keyword_optimization_suggestions: List[str] = Field(default_factory=list, description="ATS keyword density optimizations")
    project_improvement_suggestions: List[str] = Field(default_factory=list, description="Enhancements for project descriptions and metrics")


class FullAnalysisReportData(BaseModel):
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    ats_score: float
    match_percentage: float
    parsed_resume: Optional[Dict[str, Any]] = None
    skill_match: SkillMatchResult
    ats_breakdown: ATSScoreBreakdown
    interview_questions: InterviewQuestionsResult
    improvements: ResumeImprovementResult


class AnalysisRunRequest(BaseModel):
    resume_id: int = Field(..., description="ID of the uploaded resume to analyze")
    jd_id: int = Field(..., description="ID of the target Job Description")


class AnalysisReportOut(BaseModel):
    id: int
    resume_id: int
    jd_id: int
    ats_score: float
    match_percentage: float
    report_json: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
