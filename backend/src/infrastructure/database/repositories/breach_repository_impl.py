"""Breach repository implementation."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.breach import Breach
from ....domain.repositories import BreachRepository
from ..models.breach_model import BreachModel


class BreachRepositoryImpl(BreachRepository):
    """SQLAlchemy implementation of breach repository."""
    
    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session
    
    def _to_entity(self, model: BreachModel) -> Breach:
        """Convert database model to domain entity."""
        return Breach(
            id=model.id,
            name=model.name,
            domain=model.domain,
            breach_date=model.breach_date,
            added_date=model.added_date,
            modified_date=model.modified_date,
            pwn_count=model.pwn_count,
            description=model.description,
            data_classes=model.data_classes or [],
            is_verified=model.is_verified,
            is_fabricated=model.is_fabricated,
            is_sensitive=model.is_sensitive,
            is_retired=model.is_retired,
            is_spam_list=model.is_spam_list,
            logo_path=model.logo_path,
            source=model.source,
            metadata=model.metadata,
        )
    
    def _to_model(self, entity: Breach) -> BreachModel:
        """Convert domain entity to database model."""
        return BreachModel(
            id=entity.id,
            name=entity.name,
            domain=entity.domain,
            breach_date=entity.breach_date,
            added_date=entity.added_date,
            modified_date=entity.modified_date,
            pwn_count=entity.pwn_count,
            description=entity.description,
            data_classes=entity.data_classes,
            is_verified=entity.is_verified,
            is_fabricated=entity.is_fabricated,
            is_sensitive=entity.is_sensitive,
            is_retired=entity.is_retired,
            is_spam_list=entity.is_spam_list,
            logo_path=entity.logo_path,
            source=entity.source,
            metadata=entity.metadata,
        )
    
    async def create(self, breach: Breach) -> Breach:
        """Create a new breach."""
        model = self._to_model(breach)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, breach_id: UUID) -> Optional[Breach]:
        """Get breach by ID."""
        result = await self.session.execute(
            select(BreachModel).where(BreachModel.id == breach_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_name(self, name: str) -> Optional[Breach]:
        """Get breach by name."""
        result = await self.session.execute(
            select(BreachModel).where(BreachModel.name == name)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Breach]:
        """Get all breaches with pagination."""
        result = await self.session.execute(
            select(BreachModel)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update(self, breach: Breach) -> Breach:
        """Update existing breach."""
        model = await self.session.get(BreachModel, breach.id)
        if not model:
            raise ValueError(f"Breach with ID {breach.id} not found")
        
        # Update fields
        for key, value in breach.__dict__.items():
            if key != "id":
                setattr(model, key, value)
        
        model.modified_date = breach.modified_date
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, breach_id: UUID) -> bool:
        """Delete breach by ID."""
        model = await self.session.get(BreachModel, breach_id)
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True
    
    async def search(self, query: str) -> List[Breach]:
        """Search breaches by query."""
        result = await self.session.execute(
            select(BreachModel).where(
                BreachModel.name.ilike(f"%{query}%")
                | BreachModel.domain.ilike(f"%{query}%")
            )
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def get_recent(self, days: int = 30) -> List[Breach]:
        """Get recent breaches."""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(BreachModel).where(BreachModel.added_date >= cutoff_date)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def count_all(self) -> int:
        """Count all breaches."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(BreachModel.id))
        )
        return result.scalar() or 0
    
    async def count_by_source(self, source: str) -> int:
        """Count breaches by source."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(BreachModel.id)).where(BreachModel.source == source)
        )
        return result.scalar() or 0
