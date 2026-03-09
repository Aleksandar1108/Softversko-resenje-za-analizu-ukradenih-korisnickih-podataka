"""FastAPI application main file."""
import logging
import sys
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]
)
from src.api.middleware import (
    general_exception_handler,
    http_exception_handler,
    rate_limit_middleware,
    validation_exception_handler,
)
from src.api.routes import (
    analysis_router,
    breach_router,
    data_collection_router,
    ml_analysis_router,
    notification_router,
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

# CORS middleware - MUST be before other middleware
# Allow all origins for development (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging."""
    import sys
    print(f"\n{'='*60}", file=sys.stderr, flush=True)
    print(f"REQUEST: {request.method} {request.url.path}", file=sys.stderr, flush=True)
    print(f"Query params: {dict(request.query_params)}", file=sys.stderr, flush=True)
    if request.url.path == "/api/v1/users/check-email":
        print(f"⚠️ CHECK EMAIL ENDPOINT CALLED!", file=sys.stderr, flush=True)
    print(f"{'='*60}\n", file=sys.stderr, flush=True)
    
    response = await call_next(request)
    
    print(f"RESPONSE: {response.status_code} for {request.method} {request.url.path}", file=sys.stderr, flush=True)
    
    return response

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
app.include_router(ml_analysis_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Breach Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle OPTIONS requests for CORS."""
    return {"message": "OK"}


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        from src.infrastructure.database.database import async_engine
        from src.infrastructure.database.models.base import Base
        from src.infrastructure.database.models import breach_model, credential_model, user_model
        
        # Create tables if they don't exist (SQLite)
        if "sqlite" in async_engine.url.drivername:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("Database tables initialized!")
    except Exception as e:
        print(f"Database initialization warning: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
