"""Credential repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.credential import Credential


class CredentialRepository(ABC):
    """Interface for credential repository."""
    
    @abstractmethod
    async def create(self, credential: Credential) -> Credential:
        """Create a new credential."""
        pass
    
    @abstractmethod
    async def get_by_id(self, credential_id: UUID) -> Optional[Credential]:
        """Get credential by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> List[Credential]:
        """Get all credentials for an email."""
        pass
    
    @abstractmethod
    async def get_by_breach_id(self, breach_id: UUID) -> List[Credential]:
        """Get all credentials for a breach."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Credential]:
        """Get all credentials with pagination."""
        pass
    
    @abstractmethod
    async def update(self, credential: Credential) -> Credential:
        """Update existing credential."""
        pass
    
    @abstractmethod
    async def get_weak_passwords(self, threshold: int = 30) -> List[Credential]:
        """Get credentials with weak passwords."""
        pass
    
    @abstractmethod
    async def get_high_risk(self, threshold: float = 7.0) -> List[Credential]:
        """Get credentials with high risk score."""
        pass
