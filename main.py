import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from app.database.session import engine
from app.database.base import Base
import app.models  # Ensure all SQLAlchemy models are registered
from app.routers import (
    auth_router,
    resume_router,
    jd_router,
    analysis_router,
    rag_router,
    health_router,
    web_ui_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle management.
    """
    logger.info(f"Starting {settings.APP_NAME} in '{settings.APP_ENV}' mode...")
    
    # Auto-create database tables if not existing
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("SQLAlchemy database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables on startup: {e}")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description=(
        "Production-Ready Agentic AI Recruitment Assistant built with FastAPI, PostgreSQL, "
        "SQLAlchemy, JWT Authentication, Google Gemini API, LangChain, and ChromaDB.\n\n"
        "### Key Capabilities:\n"
        "- 📑 **Resume Parsing Agent**: Extract candidate contact, skills, experience, projects, and education.\n"
        "- 🎯 **Skill Matching Agent**: Compare candidate skills against target Job Descriptions.\n"
        "- 📊 **ATS Scoring Agent**: Calculate weighted ATS score (50% Skill, 20% Projects, 20% Experience, 10% Education).\n"
        "- 🎤 **Interview Question Generator Agent**: Generate Technical, Project, Behavioral, and HR interview questions.\n"
        "- 🚀 **Resume Improvement Agent**: Suggest missing skill acquisitions and ATS keyword enhancements.\n"
        "- 🔍 **RAG & Semantic Search**: Semantic candidate and Job Description vector search with ChromaDB."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# ==========================================
# CORS Middleware
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Request Timing & Correlation ID Middleware
# ==========================================
@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - "
        f"Latency: {process_time:.2f}ms [ReqID: {request_id[:8]}]"
    )
    return response


# ==========================================
# Exception Handlers Registration
# ==========================================
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# ==========================================
# Router Registrations
# ==========================================
# Web UI Dashboard (Root, /dashboard, /upload)
app.include_router(web_ui_router)

# Health check
app.include_router(health_router)

# Versioned API Routers
api_v1 = settings.API_V1_PREFIX
app.include_router(auth_router, prefix=api_v1)
app.include_router(resume_router, prefix=api_v1)
app.include_router(jd_router, prefix=api_v1)
app.include_router(analysis_router, prefix=api_v1)
app.include_router(rag_router, prefix=api_v1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
