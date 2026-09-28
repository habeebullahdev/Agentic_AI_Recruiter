from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.schemas.resume import ResumeOut, ResumeSummaryOut
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.parser import ResumeService
from app.core.dependencies import get_current_user, get_optional_current_user, require_roles
from app.core.exceptions import EntityNotFoundException, PermissionDeniedException
from app.core.logging import logger

router = APIRouter(prefix="/resume", tags=["Resume Management"])
resume_service = ResumeService()


@router.post(
    "/upload",
    response_model=APIResponse[ResumeOut],
    status_code=status.HTTP_201_CREATED,
    summary="Upload and parse Resume PDF",
    description="Uploads a PDF resume, extracts raw text, executes the Gemini ResumeAgent to extract structured candidate profile, stores in PostgreSQL, and indexes in ChromaDB."
)
async def upload_resume(
    file: UploadFile = File(..., description="PDF resume file to process"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    logger.info(f"Received resume upload request: '{file.filename}' by user: {current_user.email if current_user else 'Anonymous'}")
    resume = await resume_service.process_and_create_resume(
        db=db,
        file=file,
        current_user=current_user
    )
    return APIResponse(
        success=True,
        message="Resume uploaded and parsed successfully by ResumeAgent.",
        data=ResumeOut.model_validate(resume)
    )


@router.get(
    "/{id}",
    response_model=APIResponse[ResumeOut],
    summary="Get Resume by ID",
    description="Retrieves a stored resume including its extracted text and parsed candidate profile data."
)
def get_resume(
    id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    resume = resume_service.get_resume_by_id(db, id)
    # Check permissions if candidate user
    if current_user and current_user.role == UserRole.CANDIDATE and resume.user_id and resume.user_id != current_user.id:
        raise PermissionDeniedException("You do not have access to this resume.")

    return APIResponse(
        success=True,
        message="Resume retrieved successfully.",
        data=ResumeOut.model_validate(resume)
    )


@router.get(
    "/",
    response_model=PaginatedResponse[ResumeSummaryOut],
    summary="List all resumes with pagination",
    description="Lists uploaded resumes with pagination support. Recruiters and Admins can view all; Candidates view their own."
)
def list_resumes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    query = db.query(Resume)
    if current_user and current_user.role == UserRole.CANDIDATE:
        query = query.filter(Resume.user_id == current_user.id)

    total = query.count()
    items = query.order_by(Resume.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[ResumeSummaryOut.model_validate(r) for r in items]
    )


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    summary="Delete Resume by ID",
    description="Deletes a resume from PostgreSQL and ChromaDB vector store."
)
def delete_resume(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = resume_service.get_resume_by_id(db, id)
    if current_user.role == UserRole.CANDIDATE and resume.user_id != current_user.id:
        raise PermissionDeniedException("You cannot delete a resume that does not belong to you.")

    resume_service.delete_resume(db, id)
    return APIResponse(
        success=True,
        message=f"Resume {id} deleted successfully.",
        data=None
    )
