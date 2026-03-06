"""User API routes."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_management.check_email_breach import CheckEmailBreachUseCase
from src.application.use_cases.user_management.get_user_breaches import GetUserBreachesUseCase
from src.application.use_cases.user_management.login_user import LoginUserUseCase
from src.application.use_cases.user_management.register_user import RegisterUserUseCase
from src.config.dependencies import (
    get_breach_repository,
    get_credential_repository,
    get_hibp_client,
    get_password_hasher,
    get_user_repository,
)
from src.infrastructure.database.database import get_db
from src.api.middleware.auth_middleware import get_current_user_id
from src.api.schemas.user_schemas import (
    EmailCheckRequest,
    EmailCheckResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    try:
        # Try to get database connection
        try:
            user_repo = await get_user_repository(db)
            password_hasher = get_password_hasher()
            
            use_case = RegisterUserUseCase(user_repo, password_hasher)
            
            user = await use_case.execute(
                email=user_data.email,
                password=user_data.password,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            
            # Generate JWT token for new user
            import jwt
            from datetime import datetime
            from src.config.settings import settings
            
            token = jwt.encode(
                {
                    "sub": str(user.id),
                    "email": user.email,
                    "exp": datetime.utcnow().timestamp() + (settings.JWT_EXPIRATION_HOURS * 3600),
                },
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM,
            )
            
            return {
                "token": token,
                "user": UserResponse.model_validate(user),
            }
        except Exception as db_error:
            # If database fails, log and return error
            import traceback
            print(f"Database error in register_user: {db_error}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(db_error)}. Please check database connection.",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error in register_user: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


@router.post("/login", response_model=dict)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login user and return JWT token."""
    user_repo = await get_user_repository(db)
    password_hasher = get_password_hasher()
    
    use_case = LoginUserUseCase(user_repo, password_hasher)
    
    try:
        result = await use_case.execute(
            email=login_data.email,
            password=login_data.password,
        )
        return {
            "token": result["token"],
            "user": UserResponse.model_validate(result["user"]),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/check-email", response_model=EmailCheckResponse)
async def check_email_breach(
    request: EmailCheckRequest,
):
    """Check if email has been breached."""
    try:
        hibp_client = get_hibp_client()
        
        # Get breaches directly from HIBP API (works without database)
        breaches_data = await hibp_client.get_breaches_for_email(request.email)
        breaches = breaches_data if breaches_data else []
        
        # Calculate statistics (without database for now - can be enhanced later)
        total_breaches = len(breaches)
        
        return EmailCheckResponse(
            email=request.email,
            is_breached=total_breaches > 0,
            total_breaches=total_breaches,
            breaches=[
                {
                    "id": str(b.id) if hasattr(b, 'id') and b.id else f"breach-{i}",
                    "name": b.name if hasattr(b, 'name') else str(b),
                    "domain": b.domain if hasattr(b, 'domain') else None,
                    "breach_date": b.breach_date.isoformat() if hasattr(b, 'breach_date') and b.breach_date else None,
                    "data_classes": b.data_classes if hasattr(b, 'data_classes') else [],
                }
                for i, b in enumerate(breaches)
            ],
            statistics={
                "total_credentials": 0,  # Will be populated when database is available
                "weak_passwords": 0,
                "high_risk_credentials": 0,
            },
        )
    except Exception as e:
        # Fallback: return basic response even if everything fails
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in check_email_breach: {error_msg}")
        print(traceback_str)
        
        # Return safe response
        return EmailCheckResponse(
            email=request.email,
            is_breached=False,
            total_breaches=0,
            breaches=[],
            statistics={
                "total_credentials": 0,
                "weak_passwords": 0,
                "high_risk_credentials": 0,
            },
        )


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
    
    from src.api.schemas.breach_schemas import BreachResponse
    return [BreachResponse.model_validate(b) for b in breaches]
