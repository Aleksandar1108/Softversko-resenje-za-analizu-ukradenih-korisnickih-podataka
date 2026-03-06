"""Use case for getting user breaches."""
from typing import List
from uuid import UUID

from ....domain.entities.breach import Breach
from ....domain.repositories import BreachRepository, CredentialRepository, UserRepository


class GetUserBreachesUseCase:
    """Use case for getting all breaches for a user."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        credential_repository: CredentialRepository,
        breach_repository: BreachRepository,
    ):
        """Initialize use case with dependencies."""
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.breach_repository = breach_repository
    
    async def execute(self, user_id: UUID) -> List[Breach]:
        """
        Get all breaches for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of breaches affecting the user
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Get credentials for user's email
        credentials = await self.credential_repository.get_by_email(user.email)
        
        # Get unique breach IDs
        breach_ids = set(c.breach_id for c in credentials)
        
        # Fetch breaches
        breaches = []
        for breach_id in breach_ids:
            breach = await self.breach_repository.get_by_id(breach_id)
            if breach:
                breaches.append(breach)
        
        return breaches
