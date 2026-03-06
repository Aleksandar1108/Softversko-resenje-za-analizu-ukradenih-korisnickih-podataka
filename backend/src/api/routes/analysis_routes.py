"""Analysis API routes."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.analysis.analyze_credentials import AnalyzeCredentialsUseCase
from src.application.use_cases.analysis.generate_recommendations import GenerateRecommendationsUseCase
from src.config.dependencies import (
    get_credential_repository,
    get_password_analyzer,
    get_pattern_analyzer,
    get_password_classifier,
    get_user_repository,
)
from src.infrastructure.database.database import get_db
from src.infrastructure.ml.models.pattern_analyzer import PatternAnalyzer
from src.infrastructure.ml.models.password_classifier import PasswordClassifier
from src.api.middleware.auth_middleware import get_current_user_id
from src.api.schemas.credential_schemas import (
    CredentialAnalysisRequest,
    CredentialAnalysisResponse,
)

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/credentials/{credential_id}", response_model=CredentialAnalysisResponse)
async def analyze_credential(
    credential_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Analyze a specific credential."""
    credential_repo = await get_credential_repository(db)
    password_analyzer = get_password_analyzer()
    password_classifier = PasswordClassifier()
    pattern_analyzer = PatternAnalyzer()
    
    use_case = AnalyzeCredentialsUseCase(
        credential_repo,
        password_analyzer,
        password_classifier,
        pattern_analyzer,
    )
    
    try:
        credential = await use_case.execute(credential_id)
        
        return CredentialAnalysisResponse(
            credential_id=credential.id,
            password_strength_score=credential.password_strength_score or 0,
            risk_score=credential.risk_score or 0.0,
            is_weak=credential.is_weak,
            pattern_type=credential.pattern_type,
            recommendations=credential.recommendations,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/recommendations", response_model=list)
async def get_recommendations(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get security recommendations for current user."""
    credential_repo = await get_credential_repository(db)
    user_repo = await get_user_repository(db)
    
    use_case = GenerateRecommendationsUseCase(credential_repo, user_repo)
    recommendations = await use_case.execute_for_user(user_id)
    
    return recommendations
