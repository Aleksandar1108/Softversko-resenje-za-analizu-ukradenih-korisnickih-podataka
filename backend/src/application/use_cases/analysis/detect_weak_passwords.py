"""Use case for detecting weak passwords."""
from typing import List

from ....domain.entities.credential import Credential
from ....domain.repositories import CredentialRepository
from ...services.password_analyzer_service import PasswordAnalyzerService


class DetectWeakPasswordsUseCase:
    """Use case for detecting weak passwords in credentials."""
    
    def __init__(
        self,
        credential_repository: CredentialRepository,
        password_analyzer: PasswordAnalyzerService,
    ):
        """Initialize use case with dependencies."""
        self.credential_repository = credential_repository
        self.password_analyzer = password_analyzer
    
    async def execute(self, limit: int = 1000) -> List[Credential]:
        """
        Detect weak passwords in credentials.
        
        Args:
            limit: Maximum number of credentials to check
            
        Returns:
            List of credentials with weak passwords
        """
        # Get credentials without analysis
        credentials = await self.credential_repository.get_unanalyzed(limit=limit)
        
        weak_passwords = []
        for credential in credentials:
            if credential.password_hash:
                strength = await self.password_analyzer.analyze_password_strength(
                    credential.password_hash
                )
                
                if strength.level.value == "weak":
                    credential.is_weak = True
                    credential.password_strength_score = strength.score
                    await self.credential_repository.update(credential)
                    weak_passwords.append(credential)
        
        return weak_passwords
