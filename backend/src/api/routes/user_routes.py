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
from pydantic import BaseModel
from src.infrastructure.database.database import get_db
from src.api.middleware.auth_middleware import get_current_user_id, get_optional_user_id
from typing import Optional
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


@router.post("/check-email")
async def check_email_breach(
    request: EmailCheckRequest,
    user_id: Optional[UUID] = Depends(get_optional_user_id),
    db: Optional[AsyncSession] = Depends(get_db),
):
    """Check if email has been breached."""
    import sys
    print(f"\n{'='*60}", file=sys.stderr, flush=True)
    print(f"=== CHECK EMAIL BREACH ===", file=sys.stderr, flush=True)
    print(f"Email: {request.email}", file=sys.stderr, flush=True)
    print(f"User ID: {user_id}", file=sys.stderr, flush=True)
    print(f"DB Session: {db is not None}", file=sys.stderr, flush=True)
    print(f"{'='*60}\n", file=sys.stderr, flush=True)
    
    print(f"\n{'='*60}")
    print(f"=== CHECK EMAIL BREACH ===")
    print(f"Email: {request.email}")
    print(f"User ID: {user_id}")
    print(f"DB Session: {db is not None}")
    print(f"{'='*60}\n")
    
    breaches = []
    try:
        # Get HIBP client safely
        hibp_client = None
        try:
            print(f"Getting HIBP client...")
            hibp_client = get_hibp_client()
            print(f"HIBP client obtained: {hibp_client is not None}")
        except Exception as client_error:
            print(f"❌ Error getting HIBP client: {client_error}")
            import traceback
            print(traceback.format_exc())
            # Continue with empty breaches list
        
        # Get breaches directly from HIBP API (works without database)
        if hibp_client:
            print(f"Calling HIBP API for email: {request.email}")
            try:
                breaches_data = await hibp_client.get_breaches_for_email(request.email)
                print(f"HIBP API returned: {len(breaches_data) if breaches_data else 0} breaches")
                breaches = breaches_data if breaches_data else []
                print(f"Breaches list length: {len(breaches)}")
            except Exception as api_error:
                print(f"❌ Error calling HIBP API: {api_error}")
                import traceback
                print(traceback.format_exc())
                # Continue with empty breaches list
                breaches = []
        else:
            print(f"❌ HIBP client is None - cannot check email")
            breaches = []
        
        # Calculate statistics (without database for now - can be enhanced later)
        total_breaches = len(breaches)
        print(f"Total breaches found: {total_breaches}")
        
        # If user is logged in and breaches found, save to database and create notifications
        if user_id and total_breaches > 0 and db:
            try:
                from datetime import datetime
                from uuid import uuid4
                from src.config.dependencies import get_notification_queue, get_breach_repository
                from src.domain.entities.notification import Notification
                from src.infrastructure.database.models.user_breach_model import UserBreachModel
                from sqlalchemy import select
                
                breach_repo = await get_breach_repository(db)
                notification_queue = await get_notification_queue(db)
                
                # Save breaches to database and create user-breach relationships
                for breach in breaches:
                    try:
                        breach_name = breach.name if hasattr(breach, 'name') else 'Unknown'
                        
                        # Check if breach exists in database
                        existing_breach = await breach_repo.get_by_name(breach_name)
                        
                        if existing_breach:
                            breach_id = existing_breach.id
                        else:
                            # Create breach in database if it doesn't exist
                            from src.domain.entities.breach import Breach
                            
                            new_breach = Breach(
                                id=None,
                                name=breach_name,
                                domain=breach.domain if hasattr(breach, 'domain') else None,
                                breach_date=breach.breach_date if hasattr(breach, 'breach_date') and breach.breach_date else None,
                                added_date=datetime.utcnow(),
                                modified_date=None,
                                pwn_count=None,
                                description=None,
                                data_classes=breach.data_classes if hasattr(breach, 'data_classes') else [],
                                is_verified=False,
                                is_fabricated=False,
                                is_sensitive=False,
                                is_retired=False,
                                is_spam_list=False,
                                logo_path=None,
                                source='hibp',
                                metadata=None,
                            )
                            saved_breach = await breach_repo.create(new_breach)
                            breach_id = saved_breach.id
                        
                        # Create or update user-breach relationship
                        result = await db.execute(
                            select(UserBreachModel).where(
                                UserBreachModel.user_id == user_id,
                                UserBreachModel.breach_id == breach_id
                            )
                        )
                        user_breach = result.scalar_one_or_none()
                        
                        is_new_user_breach = False
                        if not user_breach:
                            # Create new user-breach relationship
                            is_new_user_breach = True
                            user_breach = UserBreachModel(
                                id=uuid4(),
                                user_id=user_id,
                                breach_id=breach_id,
                                notified_at=datetime.utcnow(),
                                notification_sent=False,
                                acknowledged_at=None,
                                created_at=datetime.utcnow(),
                            )
                            db.add(user_breach)
                            await db.flush()
                        
                        # Only create notification if this is a new user-breach relationship
                        # to avoid duplicate notifications
                        if is_new_user_breach:
                            notification = Notification(
                                id=uuid4(),
                                user_id=user_id,
                                type="breach_alert",
                                title=f"Email pronađen u breach-u: {breach_name}",
                                message=f"Vaš email {request.email} je pronađen u data breach-u. Preporučujemo da promenite lozinku.",
                                is_read=False,
                                priority="high",
                                metadata={
                                    "breach_name": breach_name,
                                    "breach_date": breach.breach_date.isoformat() if hasattr(breach, 'breach_date') and breach.breach_date else None,
                                    "data_classes": breach.data_classes if hasattr(breach, 'data_classes') else [],
                                },
                                created_at=datetime.utcnow(),
                                read_at=None,
                            )
                            await notification_queue.enqueue(notification)
                            
                            # Mark notification as sent
                            user_breach.notification_sent = True
                            user_breach.notified_at = datetime.utcnow()
                            await db.flush()
                        
                    except Exception as breach_save_error:
                        print(f"Error saving breach/user-breach relationship: {breach_save_error}")
                        import traceback
                        print(traceback.format_exc())
                        # Continue with next breach even if this one fails
                        continue
                
                # Commit all changes
                try:
                    await db.commit()
                    print(f"✅ Saved {total_breaches} breaches and created notifications for user {user_id}")
                except Exception as commit_error:
                    print(f"❌ Error committing to database: {commit_error}")
                    import traceback
                    print(traceback.format_exc())
                    try:
                        await db.rollback()
                        print("✅ Rollback successful")
                    except Exception as rollback_error:
                        print(f"❌ Error during rollback: {rollback_error}")
                    # Continue even if commit fails - don't break the response
                
            except Exception as db_error:
                print(f"❌ Error saving to database: {db_error}")
                import traceback
                print(traceback.format_exc())
                try:
                    if db:
                        await db.rollback()
                except Exception as rollback_error:
                    print(f"❌ Error rolling back: {rollback_error}")
                # Continue even if db fails
        
        # Parse breaches safely
        breaches_list = []
        for i, b in enumerate(breaches):
            try:
                breach_dict = {
                    "id": str(b.id) if hasattr(b, 'id') and b.id else f"breach-{i}",
                    "name": getattr(b, 'name', 'Unknown') if hasattr(b, 'name') else 'Unknown',
                    "domain": getattr(b, 'domain', None) if hasattr(b, 'domain') else None,
                    "breach_date": None,
                    "data_classes": getattr(b, 'data_classes', []) if hasattr(b, 'data_classes') else [],
                }
                
                # Safely parse breach_date
                if hasattr(b, 'breach_date') and b.breach_date:
                    try:
                        if hasattr(b.breach_date, 'isoformat'):
                            breach_dict["breach_date"] = b.breach_date.isoformat()
                        else:
                            breach_dict["breach_date"] = str(b.breach_date)
                    except Exception:
                        breach_dict["breach_date"] = None
                
                breaches_list.append(breach_dict)
            except Exception as parse_error:
                # Skip invalid breach entries
                print(f"Error parsing breach {i}: {parse_error}")
                continue
        
        response_data = EmailCheckResponse(
            email=request.email,
            is_breached=total_breaches > 0,
            total_breaches=total_breaches,
            breaches=breaches_list,
            statistics={
                "total_credentials": 0,  # Will be populated when database is available
                "weak_passwords": 0,
                "high_risk_credentials": 0,
            },
        )
        
        return {
            "success": True,
            "data": response_data.model_dump(),
        }
    except Exception as e:
        # Fallback: return basic response even if everything fails
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in check_email_breach: {error_msg}")
        print(traceback_str)
        
        # Return safe response
        response_data = EmailCheckResponse(
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
        
        return {
            "success": True,
            "data": response_data.model_dump(),
        }


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


class PasswordCheckRequest(BaseModel):
    """Schema for password check request."""
    password: str


@router.post("/check-password")
async def check_password_breach(
    request: PasswordCheckRequest,
):
    """Check if password has been breached using HIBP Password API."""
    try:
        hibp_client = get_hibp_client()
        result = await hibp_client.check_password_breached(request.password)
        
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        import traceback
        print(f"Error in check_password_breach: {e}")
        print(traceback.format_exc())
        
        return {
            "success": True,
            "data": {
                "is_breached": False,
                "count": 0,
                "message": f"Unable to check password: {str(e)}",
            },
        }
