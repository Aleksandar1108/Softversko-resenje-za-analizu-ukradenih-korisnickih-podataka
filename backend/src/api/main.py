"""FastAPI application main file."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from ...config.settings import settings
from .middleware import (
    general_exception_handler,
    http_exception_handler,
    rate_limit_middleware,
    validation_exception_handler,
)
from .routes import (
    analysis_router,
    breach_router,
    data_collection_router,
    reporting_router,
    user_router,
)

app = FastAPI(
    title="Breach Analyzer API",
    description="API for analyzing compromised credentials",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routers
app.include_router(breach_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(reporting_router, prefix="/api/v1")
app.include_router(data_collection_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Breach Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
