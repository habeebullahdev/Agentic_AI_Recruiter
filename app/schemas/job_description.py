from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class JobDescriptionBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, example="Senior Backend Engineer")
    jd_text: str = Field(..., min_length=20, example="We are seeking a Senior FastAPI & Python Backend Engineer...")
    required_skills: Optional[List[str]] = Field(default_factory=list, example=["Python", "FastAPI", "PostgreSQL", "Docker"])


class JobDescriptionCreate(JobDescriptionBase):
    pass


class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    jd_text: Optional[str] = Field(None, min_length=20)
    required_skills: Optional[List[str]] = None


class JobDescriptionOut(JobDescriptionBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobDescriptionOption(BaseModel):
    id: int
    title: str
