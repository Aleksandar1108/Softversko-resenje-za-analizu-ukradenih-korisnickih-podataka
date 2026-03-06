"""User API routes."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.use_cases.user_management.check_email_breach import CheckEmailBreachUseCase
from ...application.use_cases.user_management.get_user_breaches import GetUserBreachesUseCase
from ...application.use_cases.user_management.register_user import RegisterUserUseCase
from ...config.dependencies import (
    get_breach_repository,
    get_credential_repository,
    get_hibp_client,
    get_password_hasher,
    get_user_repository,
)
from ...infrastructure.database.database import get_db
from ..middleware.auth_middleware import get_current_user_id
from ..schemas.user_schemas import (
    EmailCheckRequest,
    EmailCheckResponse,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    user_repo = await get_user_repository(db)
    password_hasher = get_password_hasher()
    
    use_case = RegisterUserUseCase(user_repo, password_hasher)
    
    try:
        user = await use_case.execute(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/check-email", response_model=EmailCheckResponse)
async def check_email_breach(
    request: EmailCheckRequest,
    db: AsyncSession = Depends(get_db),
):
    """Check if email has been breached."""
    hibp_client = get_hibp_client()
    breach_repo = await get_breach_repository(db)
    credential_repo = await get_credential_repository(db)
    
    from ...application.use_cases.data_collection.collect_hibp_data import CollectHIBPDataUseCase
    
    collect_use_case = CollectHIBPDataUseCase(hibp_client, breach_repo, credential_repo)
    check_use_case = CheckEmailBreachUseCase(collect_use_case, breach_repo, credential_repo)
    
    result = await check_use_case.execute(request.email)
    return EmailCheckResponse(**result)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get current user information."""
    user_repo = await get_user_repository(db)
    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserResponse.model_validate(user)


@router.get("/breaches", response_model=list)
async def get_user_breaches(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get all breaches for current user."""
    user_repo = await get_user_repository(db)
    credential_repo = await get_credential_repository(db)
    breach_repo = await get_breach_repository(db)
    
    use_case = GetUserBreachesUseCase(user_repo, credential_repo, breach_repo)
    breaches = await use_case.execute(user_id)
    
    from ..schemas.breach_schemas import BreachResponse
    return [BreachResponse.model_validate(b) for b in breaches]
