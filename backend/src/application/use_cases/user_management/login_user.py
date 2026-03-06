"""Use case for user login."""
from datetime import datetime
from uuid import UUID

from src.domain.entities.user import User
from src.domain.repositories import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.database.password_hasher import PasswordHasher
import jwt
from src.config.settings import settings


class LoginUserUseCase:
    """Use case for user login."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        """Initialize use case with dependencies."""
        self.user_repository = user_repository
        self.password_hasher = password_hasher
    
    async def execute(
        self,
        email: str,
        password: str,
    ) -> dict:
        """
        Login user and return JWT token.
        
        Args:
            email: User email address
            password: User password (plain text)
            
        Returns:
            Dictionary with token and user data
        """
        # Validate email
        email_obj = Email(email)
        
        # Get user by email
        user = await self.user_repository.get_by_email(email_obj.value)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        # Verify password
        is_valid = await self.password_hasher.verify_password(password, user.password_hash)
        if not is_valid:
            raise ValueError("Invalid email or password")
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.user_repository.update(user)
        
        # Generate JWT token
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
            "user": user,
        }
