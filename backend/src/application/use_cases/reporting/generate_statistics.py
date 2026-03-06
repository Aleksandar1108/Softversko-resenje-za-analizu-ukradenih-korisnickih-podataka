"""Use case for generating statistics."""
from typing import Dict

from ....domain.repositories import BreachRepository, CredentialRepository, UserRepository


class GenerateStatisticsUseCase:
    """Use case for generating system statistics."""
    
    def __init__(
        self,
        breach_repository: BreachRepository,
        credential_repository: CredentialRepository,
        user_repository: UserRepository,
    ):
        """Initialize use case with dependencies."""
        self.breach_repository = breach_repository
        self.credential_repository = credential_repository
        self.user_repository = user_repository
    
    async def execute(self) -> Dict:
        """
        Generate overall system statistics.
        
        Returns:
            Dictionary with system statistics
        """
        # Get counts
        total_breaches = await self.breach_repository.count_all()
        total_credentials = await self.credential_repository.count_all()
        total_users = await self.user_repository.count_all()
        
        # Get weak password statistics
        weak_passwords = await self.credential_repository.count_weak_passwords()
        weak_percentage = (
            (weak_passwords / total_credentials * 100) 
            if total_credentials > 0 else 0
        )
        
        # Get risk statistics
        high_risk = await self.credential_repository.count_high_risk()
        high_risk_percentage = (
            (high_risk / total_credentials * 100)
            if total_credentials > 0 else 0
        )
        
        # Get breach sources
        hibp_breaches = await self.breach_repository.count_by_source("hibp")
        scraped_breaches = await self.breach_repository.count_by_source("scraped")
        
        return {
            "total_breaches": total_breaches,
            "total_credentials": total_credentials,
            "total_users": total_users,
            "weak_passwords": {
                "count": weak_passwords,
                "percentage": round(weak_percentage, 2),
            },
            "high_risk_credentials": {
                "count": high_risk,
                "percentage": round(high_risk_percentage, 2),
            },
            "breach_sources": {
                "hibp": hibp_breaches,
                "scraped": scraped_breaches,
            },
        }
