from fastapi import APIRouter, Depends
from app.schemas.rag import (
    RAGResumeSearchRequest, RAGResumeSearchResponse,
    RAGJDSearchRequest, RAGJDSearchResponse
)
from app.schemas.common import APIResponse
from app.services.rag_service import rag_service
from app.core.logging import logger

router = APIRouter(prefix="/rag", tags=["RAG & Semantic Search"])


@router.post(
    "/search-resumes",
    response_model=APIResponse[RAGResumeSearchResponse],
    summary="Semantic Search Candidates & Resumes",
    description="Performs semantic vector search across candidate resumes stored in ChromaDB using dense embeddings."
)
def search_resumes(request_data: RAGResumeSearchRequest):
    logger.info(f"Executing RAG Resume Search with query: '{request_data.query}'")
    results = rag_service.search_resumes(
        query=request_data.query,
        top_k=request_data.top_k,
        where_filter=request_data.filter_metadata
    )
    response_data = RAGResumeSearchResponse(
        query=request_data.query,
        total_results=len(results),
        results=results
    )
    return APIResponse(
        success=True,
        message=f"Found {len(results)} relevant candidate resumes.",
        data=response_data
    )


@router.post(
    "/search-jds",
    response_model=APIResponse[RAGJDSearchResponse],
    summary="Semantic Search Job Descriptions",
    description="Performs semantic vector search across all open Job Descriptions."
)
def search_jds(request_data: RAGJDSearchRequest):
    logger.info(f"Executing RAG JD Search with query: '{request_data.query}'")
    results = rag_service.search_jds(
        query=request_data.query,
        top_k=request_data.top_k
    )
    response_data = RAGJDSearchResponse(
        query=request_data.query,
        total_results=len(results),
        results=results
    )
    return APIResponse(
        success=True,
        message=f"Found {len(results)} matching Job Descriptions.",
        data=response_data
    )
