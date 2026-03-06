"""Use case for collecting data from HaveIBeenPwned API."""
from typing import List
from uuid import UUID

from src.domain.entities.breach import Breach
from src.domain.repositories import BreachRepository, CredentialRepository
from src.infrastructure.external_apis.hibp_client import HIBPClient


class CollectHIBPDataUseCase:
    """Use case for collecting breach data from HIBP API."""
    
    def __init__(
        self,
        hibp_client: HIBPClient,
        breach_repository: BreachRepository,
        credential_repository: CredentialRepository,
    ):
        """Initialize use case with dependencies."""
        self.hibp_client = hibp_client
        self.breach_repository = breach_repository
        self.credential_repository = credential_repository
    
    async def execute(self, email: str) -> List[Breach]:
        """
        Collect breach data for a specific email from HIBP.
        
        Args:
            email: Email address to check
            
        Returns:
            List of breaches found for the email
        """
        # Get breaches from HIBP API
        hibp_breaches = await self.hibp_client.get_breaches_for_email(email)
        
        # Save breaches to database
        saved_breaches = []
        for hibp_breach in hibp_breaches:
            # Check if breach already exists
            existing_breach = await self.breach_repository.get_by_name(hibp_breach.name)
            
            if existing_breach:
                # Update existing breach
                breach = await self.breach_repository.update(hibp_breach)
            else:
                # Create new breach
                breach = await self.breach_repository.create(hibp_breach)
            
            saved_breaches.append(breach)
        
        return saved_breaches
    
    async def sync_all_breaches(self) -> int:
        """
        Synchronize all breaches from HIBP API.
        
        Returns:
            Number of breaches synchronized
        """
        all_breaches = await self.hibp_client.get_all_breaches()
        
        count = 0
        for breach_data in all_breaches:
            existing_breach = await self.breach_repository.get_by_name(breach_data.name)
            
            if not existing_breach:
                await self.breach_repository.create(breach_data)
                count += 1
        
        return count
