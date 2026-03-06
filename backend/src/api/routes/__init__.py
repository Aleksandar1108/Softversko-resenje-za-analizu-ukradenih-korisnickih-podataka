"""API routes."""
from .analysis_routes import router as analysis_router
from .breach_routes import router as breach_router
from .data_collection_routes import router as data_collection_router
from .reporting_routes import router as reporting_router
from .user_routes import router as user_router

__all__ = [
    "breach_router",
    "user_router",
    "analysis_router",
    "reporting_router",
    "data_collection_router",
]
