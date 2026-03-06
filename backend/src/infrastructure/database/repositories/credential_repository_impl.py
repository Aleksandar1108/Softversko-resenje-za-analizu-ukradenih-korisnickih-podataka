"""Credential repository implementation."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.credential import Credential
from ....domain.repositories import CredentialRepository
from ..models.credential_model import CredentialModel


class CredentialRepositoryImpl(CredentialRepository):
    """SQLAlchemy implementation of credential repository."""
    
    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session
    
    def _to_entity(self, model: CredentialModel) -> Credential:
        """Convert database model to domain entity."""
        return Credential(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            breach_id=model.breach_id,
            discovered_date=model.discovered_date,
            password_strength_score=model.password_strength_score,
            risk_score=model.risk_score,
            is_weak=model.is_weak,
            pattern_type=model.pattern_type,
            ml_features=model.ml_features,
            recommendations=model.recommendations or [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    def _to_model(self, entity: Credential) -> CredentialModel:
        """Convert domain entity to database model."""
        return CredentialModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            breach_id=entity.breach_id,
            discovered_date=entity.discovered_date,
            password_strength_score=entity.password_strength_score,
            risk_score=entity.risk_score,
            is_weak=entity.is_weak,
            pattern_type=entity.pattern_type,
            ml_features=entity.ml_features,
            recommendations=entity.recommendations,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    async def create(self, credential: Credential) -> Credential:
        """Create a new credential."""
        model = self._to_model(credential)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def get_by_id(self, credential_id: UUID) -> Optional[Credential]:
        """Get credential by ID."""
        result = await self.session.execute(
            select(CredentialModel).where(CredentialModel.id == credential_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> List[Credential]:
        """Get all credentials for an email."""
        result = await self.session.execute(
            select(CredentialModel).where(CredentialModel.email == email)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def get_by_breach_id(self, breach_id: UUID) -> List[Credential]:
        """Get all credentials for a breach."""
        result = await self.session.execute(
            select(CredentialModel).where(CredentialModel.breach_id == breach_id)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def update(self, credential: Credential) -> Credential:
        """Update existing credential."""
        model = await self.session.get(CredentialModel, credential.id)
        if not model:
            raise ValueError(f"Credential with ID {credential.id} not found")
        
        # Update fields
        for key, value in credential.__dict__.items():
            if key != "id":
                setattr(model, key, value)
        
        model.updated_at = datetime.utcnow()
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, credential_id: UUID) -> bool:
        """Delete credential by ID."""
        model = await self.session.get(CredentialModel, credential_id)
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True
    
    async def get_unanalyzed(self, limit: int = 1000) -> List[Credential]:
        """Get credentials that haven't been analyzed yet."""
        result = await self.session.execute(
            select(CredentialModel)
            .where(CredentialModel.password_strength_score.is_(None))
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def count_all(self) -> int:
        """Count all credentials."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(CredentialModel.id))
        )
        return result.scalar() or 0
    
    async def count_weak_passwords(self) -> int:
        """Count credentials with weak passwords."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(CredentialModel.id)).where(CredentialModel.is_weak == True)
        )
        return result.scalar() or 0
    
    async def count_high_risk(self) -> int:
        """Count credentials with high risk (>= 7.0)."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(CredentialModel.id)).where(CredentialModel.risk_score >= 7.0)
        )
        return result.scalar() or 0
    
    async def count_by_date_range(self, start_date: datetime, end_date: datetime) -> int:
        """Count credentials by date range."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(CredentialModel.id)).where(
                CredentialModel.discovered_date >= start_date,
                CredentialModel.discovered_date <= end_date,
            )
        )
        return result.scalar() or 0
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Credential]:
        """Get all credentials with pagination."""
        result = await self.session.execute(
            select(CredentialModel)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def get_weak_passwords(self, threshold: int = 30) -> List[Credential]:
        """Get credentials with weak passwords."""
        result = await self.session.execute(
            select(CredentialModel).where(
                (CredentialModel.is_weak == True)
                | (CredentialModel.password_strength_score < threshold)
            )
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
    
    async def get_high_risk(self, threshold: float = 7.0) -> List[Credential]:
        """Get credentials with high risk score."""
        result = await self.session.execute(
            select(CredentialModel).where(CredentialModel.risk_score >= threshold)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
