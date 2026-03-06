"""Error handling middleware."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error",
                "details": exc.errors(),
            },
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    import traceback
    error_details = str(exc)
    traceback_str = traceback.format_exc()
    
    # Log error for debugging
    print(f"Error in {request.url.path}: {error_details}")
    print(traceback_str)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc) if str(exc) else "An internal error occurred",
            },
        },
    )
