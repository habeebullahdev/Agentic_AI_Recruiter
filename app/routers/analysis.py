from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.analysis_report import AnalysisReport
from app.models.user import User, UserRole
from app.schemas.analysis import AnalysisRunRequest, AnalysisReportOut, FullAnalysisReportData
from app.schemas.common import APIResponse, PaginatedResponse
from app.agents.orchestrator import RecruitmentWorkflowOrchestrator
from app.core.dependencies import get_current_user, get_optional_current_user
from app.core.exceptions import EntityNotFoundException, PermissionDeniedException
from app.core.logging import logger

router = APIRouter(prefix="/analysis", tags=["Recruitment AI Analysis"])
orchestrator = RecruitmentWorkflowOrchestrator()


@router.post(
    "/run",
    response_model=APIResponse[AnalysisReportOut],
    status_code=status.HTTP_201_CREATED,
    summary="Execute Agentic AI Multi-Agent Recruitment Pipeline",
    description=(
        "Executes the full multi-agent workflow:\n"
        "1. ResumeAgent (Parse / verify candidate details)\n"
        "2. MatcherAgent (Compare skills and calculate match %)\n"
        "3. ATSAgent (Compute weighted ATS score: 50% Skill, 20% Projects, 20% Experience, 10% Education)\n"
        "4. InterviewAgent (Generate Technical, Project, Behavioral, and HR questions)\n"
        "5. ImprovementAgent (Generate resume optimization and missing skill advice)\n"
        "Stores the final report in PostgreSQL and returns the comprehensive analysis."
    )
)
async def run_recruitment_analysis(
    request_data: AnalysisRunRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    # Fetch target Resume
    resume = db.query(Resume).filter(Resume.id == request_data.resume_id).first()
    if not resume:
        raise EntityNotFoundException("Resume", request_data.resume_id)

    # Fetch target Job Description
    jd = db.query(JobDescription).filter(JobDescription.id == request_data.jd_id).first()
    if not jd:
        raise EntityNotFoundException("JobDescription", request_data.jd_id)

    logger.info(f"Running Multi-Agent Analysis: Resume #{resume.id} ('{resume.file_name}') vs JD #{jd.id} ('{jd.title}')")

    # Execute Multi-Agent Orchestrator
    report_data: FullAnalysisReportData = await orchestrator.run_full_pipeline(
        resume_text=resume.extracted_text,
        jd_title=jd.title,
        jd_text=jd.jd_text,
        existing_parsed_data=resume.parsed_data,
        required_skills=jd.required_skills
    )

    # If resume parsed_data was previously empty, update it
    if not resume.parsed_data and report_data.parsed_resume:
        resume.parsed_data = report_data.parsed_resume
        db.commit()

    # Store Analysis Report in PostgreSQL
    analysis_record = AnalysisReport(
        resume_id=resume.id,
        jd_id=jd.id,
        ats_score=report_data.ats_score,
        match_percentage=report_data.match_percentage,
        report_json=report_data.dict()
    )
    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    logger.info(f"Created AnalysisReport #{analysis_record.id} with ATS score {analysis_record.ats_score}")

    return APIResponse(
        success=True,
        message="Multi-Agent recruitment analysis completed successfully.",
        data=AnalysisReportOut.model_validate(analysis_record)
    )


@router.get(
    "/{id}",
    response_model=APIResponse[AnalysisReportOut],
    summary="Get Analysis Report by ID",
    description="Retrieves a complete stored recruitment analysis report by its ID."
)
def get_analysis_report(
    id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    report = db.query(AnalysisReport).filter(AnalysisReport.id == id).first()
    if not report:
        raise EntityNotFoundException("AnalysisReport", id)

    return APIResponse(
        success=True,
        message="Analysis report retrieved successfully.",
        data=AnalysisReportOut.model_validate(report)
    )


@router.get(
    "/resume/{resume_id}",
    response_model=APIResponse[List[AnalysisReportOut]],
    summary="Get all Analysis Reports for a specific resume",
    description="Returns all historical evaluation reports generated for a candidate's resume."
)
def get_reports_by_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    # Check resume existence
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise EntityNotFoundException("Resume", resume_id)

    reports = db.query(AnalysisReport).filter(AnalysisReport.resume_id == resume_id).order_by(AnalysisReport.created_at.desc()).all()
    return APIResponse(
        success=True,
        message=f"Found {len(reports)} analysis reports for Resume #{resume_id}.",
        data=[AnalysisReportOut.model_validate(r) for r in reports]
    )


@router.get(
    "/jd/{jd_id}/rankings",
    response_model=APIResponse[List[AnalysisReportOut]],
    summary="Get candidate rankings for a Job Description",
    description="Returns candidate analysis reports for a Job Description, ranked from highest to lowest ATS score."
)
def get_rankings_by_jd(
    jd_id: int,
    db: Session = Depends(get_db)
):
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not jd:
        raise EntityNotFoundException("JobDescription", jd_id)

    ranked_reports = db.query(AnalysisReport).filter(
        AnalysisReport.jd_id == jd_id
    ).order_by(AnalysisReport.ats_score.desc()).all()

    return APIResponse(
        success=True,
        message=f"Retrieved {len(ranked_reports)} candidate rankings for JD '{jd.title}'.",
        data=[AnalysisReportOut.model_validate(r) for r in ranked_reports]
    )
