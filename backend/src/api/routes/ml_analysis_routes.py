"""ML Analysis API routes."""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.credential_ml_service import CredentialMLService
from src.config.dependencies import get_credential_repository
from src.infrastructure.database.database import get_db
from src.api.middleware.auth_middleware import get_current_user_id

router = APIRouter(prefix="/ml-analysis", tags=["ml-analysis"])


class PasswordAnalysisRequest(BaseModel):
    """Request schema for password analysis."""
    password: str
    email: Optional[EmailStr] = None
    breach_count: int = 0


class PasswordAnalysisResponse(BaseModel):
    """Response schema for password analysis."""
    risk_score: float
    risk_level: str  # LOW, MEDIUM, HIGH
    is_weak: bool
    recommendations: List[str]
    features: dict


@router.post("/analyze-password", response_model=PasswordAnalysisResponse)
async def analyze_password(
    request: PasswordAnalysisRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Analyze a password using ML models.
    
    Returns risk_score (0-100), risk_level, and recommendations.
    """
    ml_service = CredentialMLService()
    
    try:
        analysis = ml_service.risk_analyzer.analyze_credential(
            password=request.password,
            email=request.email,
            breach_count=request.breach_count,
        )
        
        return PasswordAnalysisResponse(**analysis)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during analysis: {str(e)}",
        )


@router.post("/analyze-credential/{credential_id}")
async def analyze_credential_ml(
    credential_id: UUID,
    password: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Analyze a credential using ML models.
    
    Args:
        credential_id: ID of credential to analyze
        password: Optional plain text password (if available)
    """
    credential_repo = await get_credential_repository(db)
    credential = await credential_repo.get_by_id(credential_id)
    
    if not credential:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Credential with ID {credential_id} not found",
        )
    
    ml_service = CredentialMLService()
    
    try:
        analysis = await ml_service.analyze_credential(credential, password)
        
        # Update credential with analysis results if password provided
        if password:
            updated = await ml_service.update_credential_with_analysis(
                credential=credential,
                password=password,
                credential_repository=credential_repo,
            )
            analysis["credential_updated"] = True
        
        return {
            "success": True,
            "data": analysis,
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during analysis: {str(e)}",
        )


@router.post("/detect-weak-passwords")
async def detect_weak_passwords(
    credential_ids: List[UUID],
    passwords: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Detect weak passwords in a batch of credentials.
    
    Args:
        credential_ids: List of credential IDs to check
        passwords: Optional list of plain text passwords
    """
    credential_repo = await get_credential_repository(db)
    
    credentials = []
    for cred_id in credential_ids:
        cred = await credential_repo.get_by_id(cred_id)
        if cred:
            credentials.append(cred)
    
    ml_service = CredentialMLService()
    
    try:
        weak_credentials = await ml_service.detect_weak_passwords(
            credentials=credentials,
            passwords=passwords,
        )
        
        return {
            "success": True,
            "weak_count": len(weak_credentials),
            "weak_credentials": [
                {
                    "id": str(c.id),
                    "email": c.email,
                    "risk_score": c.risk_score,
                }
                for c in weak_credentials
            ],
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during detection: {str(e)}",
        )
