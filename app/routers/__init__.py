"""
Routers module export.
"""
from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
from app.routers.jd import router as jd_router
from app.routers.analysis import router as analysis_router
from app.routers.rag import router as rag_router
from app.routers.health import router as health_router
from app.routers.web_ui import router as web_ui_router

__all__ = [
    "auth_router",
    "resume_router",
    "jd_router",
    "analysis_router",
    "rag_router",
    "health_router",
    "web_ui_router"
]
