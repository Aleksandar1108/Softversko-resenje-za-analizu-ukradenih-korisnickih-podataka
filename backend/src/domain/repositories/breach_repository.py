"""Breach repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities.breach import Breach


class BreachRepository(ABC):
    """Interface for breach repository."""
    
    @abstractmethod
    async def create(self, breach: Breach) -> Breach:
        """Create a new breach."""
        pass
    
    @abstractmethod
    async def get_by_id(self, breach_id: UUID) -> Optional[Breach]:
        """Get breach by ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Breach]:
        """Get breach by name."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Breach]:
        """Get all breaches with pagination."""
        pass
    
    @abstractmethod
    async def update(self, breach: Breach) -> Breach:
        """Update existing breach."""
        pass
    
    @abstractmethod
    async def delete(self, breach_id: UUID) -> bool:
        """Delete breach by ID."""
        pass
    
    @abstractmethod
    async def search(self, query: str) -> List[Breach]:
        """Search breaches by query."""
        pass
    
    @abstractmethod
    async def get_recent(self, days: int = 30) -> List[Breach]:
        """Get recent breaches."""
        pass
