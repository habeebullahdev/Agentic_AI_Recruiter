from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class RAGResumeSearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Search query or skill requirements to find matching candidates")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of top results to retrieve")
    filter_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional ChromaDB metadata filter")


class RAGResumeSearchResultItem(BaseModel):
    resume_id: int
    candidate_name: Optional[str] = None
    similarity_score: float
    snippet: str
    skills: List[str] = []
    metadata: Dict[str, Any] = {}


class RAGResumeSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[RAGResumeSearchResultItem]


class RAGJDSearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Search query or candidate profile to find matching Job Descriptions")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of top results to retrieve")


class RAGJDSearchResultItem(BaseModel):
    jd_id: int
    title: str
    similarity_score: float
    snippet: str
    metadata: Dict[str, Any] = {}


class RAGJDSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[RAGJDSearchResultItem]
