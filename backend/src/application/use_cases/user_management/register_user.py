"""Use case for user registration."""
from datetime import datetime
from uuid import uuid4

from src.domain.entities.user import User
from src.domain.repositories import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.database.password_hasher import PasswordHasher


class RegisterUserUseCase:
    """Use case for registering a new user."""
    
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
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        """
        Register a new user.
        
        Args:
            email: User email address
            password: User password (plain text)
            first_name: User first name (optional)
            last_name: User last name (optional)
            
        Returns:
            Created user entity
        """
        # Validate email
        email_obj = Email(email)
        
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email_obj.value)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        password_hash = await self.password_hasher.hash_password(password)
        
        # Create user entity
        user = User(
            id=uuid4(),
            email=email_obj.value,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            email_verified=False,
            notification_preferences={
                "email": True,
                "in_app": True,
                "sms": False,
            },
            created_at=datetime.utcnow(),
            updated_at=None,
            last_login=None,
        )
        
        # Save user
        created_user = await self.user_repository.create(user)
        
        return created_user
