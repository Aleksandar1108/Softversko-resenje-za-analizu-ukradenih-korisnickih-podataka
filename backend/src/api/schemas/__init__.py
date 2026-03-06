"""API schemas."""
from .breach_schemas import BreachCreate, BreachListResponse, BreachResponse
from .credential_schemas import (
    CredentialAnalysisRequest,
    CredentialAnalysisResponse,
    CredentialResponse,
)
from .user_schemas import (
    EmailCheckRequest,
    EmailCheckResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

__all__ = [
    "BreachCreate",
    "BreachResponse",
    "BreachListResponse",
    "CredentialResponse",
    "CredentialAnalysisRequest",
    "CredentialAnalysisResponse",
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "EmailCheckRequest",
    "EmailCheckResponse",
]
