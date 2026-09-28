from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProjectItem(BaseModel):
    title: str = Field(..., description="Project name or title")
    technologies: List[str] = Field(default_factory=list, description="Technologies / tools used")
    description: str = Field(..., description="Brief description of the project and achievements")


class EducationItem(BaseModel):
    degree: str = Field(..., description="Degree or certification name")
    institution: str = Field(..., description="University, College, or School")
    year: Optional[str] = Field(None, description="Graduation year or date range")
    grade: Optional[str] = Field(None, description="GPA, percentage, or honors")


class ExperienceItem(BaseModel):
    company: str = Field(..., description="Company or Organization")
    role: str = Field(..., description="Job Title or Designation")
    duration: Optional[str] = Field(None, description="Employment duration (e.g., 2021 - 2024)")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and accomplishments")


class ParsedResumeData(BaseModel):
    name: Optional[str] = Field(None, description="Candidate full name")
    email: Optional[str] = Field(None, description="Candidate email address")
    phone: Optional[str] = Field(None, description="Candidate phone number")
    skills: List[str] = Field(default_factory=list, description="Extracted technical and soft skills")
    projects: List[ProjectItem] = Field(default_factory=list, description="Extracted project details")
    education: List[EducationItem] = Field(default_factory=list, description="Extracted academic qualifications")
    experience: List[ExperienceItem] = Field(default_factory=list, description="Extracted work history")
    summary: Optional[str] = Field(None, description="Brief professional summary")


class ResumeBase(BaseModel):
    file_name: str
    file_path: str
    extracted_text: str


class ResumeCreate(ResumeBase):
    user_id: Optional[int] = None
    parsed_data: Optional[ParsedResumeData] = None


class ResumeSummaryOut(BaseModel):
    id: int
    user_id: Optional[int]
    file_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeOut(BaseModel):
    id: int
    user_id: Optional[int]
    file_name: str
    file_path: str
    extracted_text: str
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
