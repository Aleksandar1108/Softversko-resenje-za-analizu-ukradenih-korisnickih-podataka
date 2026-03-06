"""Use case for analyzing credentials."""
from typing import List
from uuid import UUID

from src.domain.entities.credential import Credential
from src.domain.repositories import CredentialRepository
from src.infrastructure.ml.models.password_classifier import PasswordClassifier
from src.infrastructure.ml.models.pattern_analyzer import PatternAnalyzer
from src.application.services.password_analyzer_service import PasswordAnalyzerService


class AnalyzeCredentialsUseCase:
    """Use case for analyzing compromised credentials."""
    
    def __init__(
        self,
        credential_repository: CredentialRepository,
        password_analyzer: PasswordAnalyzerService,
        password_classifier: PasswordClassifier,
        pattern_analyzer: PatternAnalyzer,
    ):
        """Initialize use case with dependencies."""
        self.credential_repository = credential_repository
        self.password_analyzer = password_analyzer
        self.password_classifier = password_classifier
        self.pattern_analyzer = pattern_analyzer
    
    async def execute(self, credential_id: UUID) -> Credential:
        """
        Analyze a credential and update its analysis data.
        
        Args:
            credential_id: ID of the credential to analyze
            
        Returns:
            Updated credential with analysis data
        """
        credential = await self.credential_repository.get_by_id(credential_id)
        
        if not credential:
            raise ValueError(f"Credential with ID {credential_id} not found")
        
        # Analyze password if hash is available
        if credential.password_hash:
            # Extract password features (if possible from hash)
            # Note: In real scenario, we might need the actual password
            # For now, we'll use ML models that work with features
            
            # Get password strength
            strength = await self.password_analyzer.analyze_password_strength(
                credential.password_hash
            )
            
            # Detect patterns
            patterns = await self.pattern_analyzer.analyze(credential.password_hash)
            
            # Classify password
            classification = await self.password_classifier.classify(
                credential.password_hash
            )
            
            # Update credential with analysis results
            credential.password_strength_score = strength.score
            credential.is_weak = strength.level.value == "weak"
            credential.pattern_type = patterns.get("primary_pattern")
            credential.ml_features = {
                "strength": strength.score,
                "level": strength.level.value,
                "patterns": patterns,
                "classification": classification,
            }
        
        # Update credential in repository
        updated_credential = await self.credential_repository.update(credential)
        
        return updated_credential
    
    async def analyze_batch(self, credential_ids: List[UUID]) -> List[Credential]:
        """
        Analyze multiple credentials in batch.
        
        Args:
            credential_ids: List of credential IDs to analyze
            
        Returns:
            List of updated credentials
        """
        results = []
        for credential_id in credential_ids:
            try:
                analyzed = await self.execute(credential_id)
                results.append(analyzed)
            except Exception as e:
                # Log error and continue with next credential
                print(f"Error analyzing credential {credential_id}: {e}")
        
        return results
