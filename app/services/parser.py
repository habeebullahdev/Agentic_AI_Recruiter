from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.resume import Resume
from app.models.user import User
from app.agents.resume_agent import ResumeAgent
from app.utils.pdf_extractor import extract_text_from_pdf_bytes
from app.utils.helpers import save_upload_file
from app.services.rag_service import rag_service
from app.core.exceptions import EntityNotFoundException, FileProcessingException
from app.core.logging import logger


class ResumeService:
    """
    Business service layer for Resume processing, PDF ingestion, and Agentic extraction.
    """

    def __init__(self, resume_agent: Optional[ResumeAgent] = None):
        self.resume_agent = resume_agent or ResumeAgent()

    async def process_and_create_resume(
        self,
        db: Session,
        file: UploadFile,
        current_user: Optional[User] = None
    ) -> Resume:
        """
        Reads uploaded PDF, saves file to disk, extracts text, executes ResumeAgent parsing,
        persists to PostgreSQL, and indexes in ChromaDB vector store.
        """
        if not file.filename.lower().endswith(".pdf"):
            raise FileProcessingException("Only PDF resumes are supported.")

        content = await file.read()
        if len(content) == 0:
            raise FileProcessingException("Uploaded file is empty.")

        # Save file to disk
        saved_file_path = save_upload_file(content, file.filename)

        # Extract text from PDF
        extracted_text = extract_text_from_pdf_bytes(content, file.filename)

        # Execute Resume Parsing Agent
        parsed_data = await self.resume_agent.parse_resume(extracted_text)
        parsed_dict = parsed_data.dict()

        # Persist to Database
        db_resume = Resume(
            user_id=current_user.id if current_user else None,
            file_name=file.filename,
            file_path=saved_file_path,
            extracted_text=extracted_text,
            parsed_data=parsed_dict
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)

        # Index in ChromaDB for Semantic Search / RAG
        try:
            rag_service.index_resume(
                resume_id=db_resume.id,
                extracted_text=extracted_text,
                file_name=file.filename,
                candidate_name=parsed_dict.get("name"),
                skills=parsed_dict.get("skills", [])
            )
        except Exception as e:
            logger.warning(f"ChromaDB indexing warning for resume {db_resume.id}: {e}")

        logger.info(f"Resume ID {db_resume.id} successfully processed and stored for candidate: {parsed_dict.get('name')}")
        return db_resume

    def get_resume_by_id(self, db: Session, resume_id: int) -> Resume:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise EntityNotFoundException("Resume", resume_id)
        return resume

    def delete_resume(self, db: Session, resume_id: int) -> None:
        resume = self.get_resume_by_id(db, resume_id)
        # Delete from ChromaDB
        rag_service.delete_resume_index(resume_id)
        # Delete from DB
        db.delete(resume)
        db.commit()
        logger.info(f"Resume {resume_id} successfully deleted.")
