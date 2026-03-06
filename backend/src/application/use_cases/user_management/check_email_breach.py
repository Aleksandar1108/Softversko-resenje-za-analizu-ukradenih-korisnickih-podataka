"""Use case for checking if email is breached."""
from typing import List

from src.domain.entities.breach import Breach
from src.domain.repositories import BreachRepository, CredentialRepository
from src.domain.value_objects.email import Email
from src.application.use_cases.data_collection.collect_hibp_data import CollectHIBPDataUseCase


class CheckEmailBreachUseCase:
    """Use case for checking if an email address has been breached."""
    
    def __init__(
        self,
        collect_hibp_data: CollectHIBPDataUseCase,
        breach_repository: BreachRepository,
        credential_repository: CredentialRepository,
    ):
        """Initialize use case with dependencies."""
        self.collect_hibp_data = collect_hibp_data
        self.breach_repository = breach_repository
        self.credential_repository = credential_repository
    
    async def execute(self, email: str) -> dict:
        """
        Check if email has been breached.
        
        Args:
            email: Email address to check
            
        Returns:
            Dictionary with breach information
        """
        # Validate email
        email_obj = Email(email)
        
        # Collect breach data from HIBP
        breaches = await self.collect_hibp_data.execute(email_obj.value)
        
        # Get credentials for this email
        credentials = await self.credential_repository.get_by_email(email_obj.value)
        
        # Calculate statistics
        total_breaches = len(breaches)
        weak_passwords = sum(1 for c in credentials if c.is_weak)
        high_risk_count = sum(
            1 for c in credentials 
            if c.risk_score and c.risk_score >= 7.0
        )
        
        return {
            "email": email_obj.value,
            "is_breached": total_breaches > 0,
            "total_breaches": total_breaches,
            "breaches": [
                {
                    "id": str(b.id),
                    "name": b.name,
                    "domain": b.domain,
                    "breach_date": b.breach_date.isoformat() if b.breach_date else None,
                    "data_classes": b.data_classes,
                }
                for b in breaches
            ],
            "statistics": {
                "total_credentials": len(credentials),
                "weak_passwords": weak_passwords,
                "high_risk_credentials": high_risk_count,
            },
        }
