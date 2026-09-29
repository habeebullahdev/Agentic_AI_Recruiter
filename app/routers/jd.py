from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud.job_description import get_job_description_options
from app.models.job_description import JobDescription
from app.models.user import User, UserRole
from app.schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionUpdate,
    JobDescriptionOut,
    JobDescriptionOption,
)
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.rag_service import rag_service
from app.core.dependencies import get_current_user, get_optional_current_user, require_roles
from app.core.exceptions import EntityNotFoundException, PermissionDeniedException
from app.core.logging import logger

router = APIRouter(prefix="/jd", tags=["Job Description Management"])


@router.get(
    "/options",
    response_model=List[JobDescriptionOption],
    summary="List job roles for selection",
    description="Returns every available job description as an ID and title pair.",
)
def list_job_description_options(db: Session = Depends(get_db)):
    return get_job_description_options(db)


@router.post(
    "/create",
    response_model=APIResponse[JobDescriptionOut],
    status_code=status.HTTP_201_CREATED,
    summary="Create Job Description",
    description="Creates a new Job Description in PostgreSQL and indexes it in ChromaDB for semantic search."
)
def create_job_description(
    jd_in: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    new_jd = JobDescription(
        title=jd_in.title.strip(),
        jd_text=jd_in.jd_text.strip(),
        required_skills=jd_in.required_skills or [],
        created_by=current_user.id if current_user else None
    )
    db.add(new_jd)
    db.commit()
    db.refresh(new_jd)

    # Index in ChromaDB
    try:
        rag_service.index_jd(
            jd_id=new_jd.id,
            title=new_jd.title,
            jd_text=new_jd.jd_text,
            required_skills=new_jd.required_skills
        )
    except Exception as e:
        logger.warning(f"Failed to index JD {new_jd.id} in ChromaDB: {e}")

    logger.info(f"Created Job Description ID {new_jd.id}: '{new_jd.title}'")
    return APIResponse(
        success=True,
        message="Job Description created and indexed successfully.",
        data=JobDescriptionOut.model_validate(new_jd)
    )


@router.get(
    "/{id}",
    response_model=APIResponse[JobDescriptionOut],
    summary="Get Job Description by ID",
    description="Fetches a Job Description by its primary key ID."
)
def get_job_description(
    id: int,
    db: Session = Depends(get_db)
):
    jd = db.query(JobDescription).filter(JobDescription.id == id).first()
    if not jd:
        raise EntityNotFoundException("JobDescription", id)

    return APIResponse(
        success=True,
        message="Job Description retrieved successfully.",
        data=JobDescriptionOut.model_validate(jd)
    )


@router.get(
    "/",
    response_model=PaginatedResponse[JobDescriptionOut],
    summary="List all Job Descriptions",
    description="Lists all Job Descriptions with pagination support."
)
def list_job_descriptions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    query = db.query(JobDescription)
    total = query.count()
    items = query.order_by(JobDescription.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[JobDescriptionOut.model_validate(j) for j in items]
    )


@router.put(
    "/{id}",
    response_model=APIResponse[JobDescriptionOut],
    summary="Update Job Description",
    description="Updates title, text, or required skills of an existing Job Description."
)
def update_job_description(
    id: int,
    jd_update: JobDescriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jd = db.query(JobDescription).filter(JobDescription.id == id).first()
    if not jd:
        raise EntityNotFoundException("JobDescription", id)

    if current_user.role == UserRole.CANDIDATE:
        raise PermissionDeniedException("Candidates cannot update Job Descriptions.")

    if jd_update.title is not None:
        jd.title = jd_update.title.strip()
    if jd_update.jd_text is not None:
        jd.jd_text = jd_update.jd_text.strip()
    if jd_update.required_skills is not None:
        jd.required_skills = jd_update.required_skills

    db.commit()
    db.refresh(jd)

    # Re-index updated JD in ChromaDB
    try:
        rag_service.index_jd(
            jd_id=jd.id,
            title=jd.title,
            jd_text=jd.jd_text,
            required_skills=jd.required_skills
        )
    except Exception as e:
        logger.warning(f"Failed to re-index JD {jd.id} in ChromaDB: {e}")

    logger.info(f"Updated Job Description ID {jd.id}: '{jd.title}'")
    return APIResponse(
        success=True,
        message="Job Description updated successfully.",
        data=JobDescriptionOut.model_validate(jd)
    )


@router.delete(
    "/{id}",
    response_model=APIResponse[None],
    summary="Delete Job Description",
    description="Deletes a Job Description from PostgreSQL and ChromaDB vector store."
)
def delete_job_description(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jd = db.query(JobDescription).filter(JobDescription.id == id).first()
    if not jd:
        raise EntityNotFoundException("JobDescription", id)

    if current_user.role == UserRole.CANDIDATE:
        raise PermissionDeniedException("Candidates cannot delete Job Descriptions.")

    # Delete index
    rag_service.delete_jd_index(id)

    db.delete(jd)
    db.commit()
    logger.info(f"Deleted Job Description ID {id}")

    return APIResponse(
        success=True,
        message=f"Job Description {id} deleted successfully.",
        data=None
    )
