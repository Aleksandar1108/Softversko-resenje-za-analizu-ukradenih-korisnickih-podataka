"""User repository implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.user import User
from ....domain.repositories import UserRepository
from ..models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """SQLAlchemy implementation of user repository."""
    
    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            email_verified=model.email_verified,
            notification_preferences=model.notification_preferences or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
        )
    
    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            email_verified=entity.email_verified,
            notification_preferences=entity.notification_preferences,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_login=entity.last_login,
        )
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def update(self, user: User) -> User:
        """Update existing user."""
        model = await self.session.get(UserModel, user.id)
        if not model:
            raise ValueError(f"User with ID {user.id} not found")
        
        # Update fields
        for key, value in user.__dict__.items():
            if key != "id":
                setattr(model, key, value)
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID."""
        model = await self.session.get(UserModel, user_id)
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True
    
    async def count_all(self) -> int:
        """Count all users."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(UserModel.id))
        )
        return result.scalar() or 0
