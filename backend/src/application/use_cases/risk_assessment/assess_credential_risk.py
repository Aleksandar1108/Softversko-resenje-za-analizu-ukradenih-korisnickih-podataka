"""Use case for assessing credential risk."""
from typing import List
from uuid import UUID

from ....domain.entities.credential import Credential
from ....domain.repositories import CredentialRepository
from ....infrastructure.ml.models.risk_predictor import RiskPredictor
from ...services.risk_calculator_service import RiskCalculatorService


class AssessCredentialRiskUseCase:
    """Use case for assessing risk of compromised credentials."""
    
    def __init__(
        self,
        credential_repository: CredentialRepository,
        risk_calculator: RiskCalculatorService,
        risk_predictor: RiskPredictor,
    ):
        """Initialize use case with dependencies."""
        self.credential_repository = credential_repository
        self.risk_calculator = risk_calculator
        self.risk_predictor = risk_predictor
    
    async def execute(self, credential_id: UUID) -> Credential:
        """
        Assess risk for a specific credential.
        
        Args:
            credential_id: ID of the credential to assess
            
        Returns:
            Updated credential with risk score
        """
        credential = await self.credential_repository.get_by_id(credential_id)
        
        if not credential:
            raise ValueError(f"Credential with ID {credential_id} not found")
        
        # Calculate risk score using service
        risk_score = await self.risk_calculator.calculate_risk(credential)
        
        # Optionally use ML model for prediction
        if credential.ml_features:
            ml_risk = await self.risk_predictor.predict(credential.ml_features)
            # Combine both scores (weighted average)
            final_risk = (risk_score.value * 0.6) + (ml_risk * 0.4)
            risk_score.value = final_risk
        
        # Update credential with risk score
        credential.risk_score = risk_score.value
        credential = await self.credential_repository.update(credential)
        
        return credential
    
    async def assess_batch(self, credential_ids: List[UUID]) -> List[Credential]:
        """
        Assess risk for multiple credentials.
        
        Args:
            credential_ids: List of credential IDs to assess
            
        Returns:
            List of updated credentials with risk scores
        """
        results = []
        for credential_id in credential_ids:
            try:
                assessed = await self.execute(credential_id)
                results.append(assessed)
            except Exception as e:
                print(f"Error assessing credential {credential_id}: {e}")
        
        return results
