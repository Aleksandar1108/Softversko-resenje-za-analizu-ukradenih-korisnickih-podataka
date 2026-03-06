"""Use case for generating security recommendations."""
from typing import List
from uuid import UUID

from ....domain.entities.credential import Credential
from ....domain.repositories import CredentialRepository, UserRepository


class GenerateRecommendationsUseCase:
    """Use case for generating personalized security recommendations."""
    
    def __init__(
        self,
        credential_repository: CredentialRepository,
        user_repository: UserRepository,
    ):
        """Initialize use case with dependencies."""
        self.credential_repository = credential_repository
        self.user_repository = user_repository
    
    async def execute_for_user(self, user_id: UUID) -> List[str]:
        """
        Generate recommendations for a specific user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of security recommendations
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Get user's compromised credentials
        credentials = await self.credential_repository.get_by_email(user.email)
        
        recommendations = []
        
        # Analyze credentials and generate recommendations
        weak_count = sum(1 for c in credentials if c.is_weak)
        high_risk_count = sum(1 for c in credentials if c.risk_score and c.risk_score >= 7.0)
        
        if weak_count > 0:
            recommendations.append(
                f"Change {weak_count} weak password(s) immediately. "
                "Use a combination of uppercase, lowercase, numbers, and special characters."
            )
        
        if high_risk_count > 0:
            recommendations.append(
                f"You have {high_risk_count} credential(s) with high risk. "
                "Consider enabling two-factor authentication."
            )
        
        if len(credentials) > 5:
            recommendations.append(
                "You have been compromised in multiple breaches. "
                "Consider using a password manager to generate and store unique passwords."
            )
        
        # Check for reused passwords
        unique_passwords = len(set(c.password_hash for c in credentials if c.password_hash))
        if unique_passwords < len(credentials) / 2:
            recommendations.append(
                "You appear to be reusing passwords across multiple accounts. "
                "Use unique passwords for each account."
            )
        
        # General recommendations
        if not recommendations:
            recommendations.append(
                "Your credentials appear secure. Continue using strong, unique passwords."
            )
        
        return recommendations
    
    async def execute_for_credential(self, credential_id: UUID) -> List[str]:
        """
        Generate recommendations for a specific credential.
        
        Args:
            credential_id: ID of the credential
            
        Returns:
            List of recommendations for the credential
        """
        credential = await self.credential_repository.get_by_id(credential_id)
        if not credential:
            raise ValueError(f"Credential with ID {credential_id} not found")
        
        recommendations = []
        
        if credential.is_weak:
            recommendations.append("This password is weak. Change it immediately.")
            recommendations.append("Use at least 12 characters with mixed case, numbers, and symbols.")
        
        if credential.risk_score and credential.risk_score >= 8.0:
            recommendations.append("This credential has critical risk. Immediate action required.")
        
        if credential.pattern_type in ["common", "dictionary"]:
            recommendations.append("Avoid using common words or dictionary words in passwords.")
        
        if credential.pattern_type == "sequential":
            recommendations.append("Avoid sequential patterns (e.g., 12345, abcde) in passwords.")
        
        return recommendations
