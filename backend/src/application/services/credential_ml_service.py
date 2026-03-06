"""Service for ML-based credential analysis."""
from typing import Dict, List, Optional
from uuid import UUID

from src.domain.entities.credential import Credential
from src.domain.repositories import CredentialRepository
from src.infrastructure.ml.models.credential_risk_analyzer import CredentialRiskAnalyzer


class CredentialMLService:
    """Service for ML-based credential analysis."""
    
    def __init__(self):
        """Initialize ML service."""
        self.risk_analyzer = CredentialRiskAnalyzer()
    
    async def analyze_credential(
        self,
        credential: Credential,
        password: Optional[str] = None,
    ) -> Dict:
        """
        Analyze credential using ML models.
        
        Args:
            credential: Credential entity
            password: Optional plain text password (if available)
            
        Returns:
            Analysis results with risk_score, risk_level, and recommendations
        """
        # If password is not provided, we can't do full analysis
        # In production, you might need to decrypt or retrieve password
        if not password:
            # Use hash-based analysis (limited)
            return {
                "risk_score": 50.0,
                "risk_level": "MEDIUM",
                "is_weak": False,
                "recommendations": ["Password analysis requires plain text password"],
                "note": "Limited analysis - password hash only",
            }
        
        # Get breach count for this email
        breach_count = 0
        if credential.breach_id:
            # In production, count breaches for this email
            breach_count = 1  # Placeholder
        
        # Analyze using ML model
        analysis = self.risk_analyzer.analyze_credential(
            password=password,
            email=credential.email,
            breach_count=breach_count,
        )
        
        return analysis
    
    async def analyze_batch(
        self,
        credentials: List[Credential],
        passwords: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Analyze multiple credentials in batch.
        
        Args:
            credentials: List of credential entities
            passwords: Optional list of plain text passwords
            
        Returns:
            List of analysis results
        """
        results = []
        
        for i, credential in enumerate(credentials):
            password = passwords[i] if passwords and i < len(passwords) else None
            
            try:
                analysis = await self.analyze_credential(credential, password)
                results.append({
                    "credential_id": str(credential.id),
                    "email": credential.email,
                    **analysis,
                })
            except Exception as e:
                results.append({
                    "credential_id": str(credential.id),
                    "email": credential.email,
                    "error": str(e),
                })
        
        return results
    
    async def detect_weak_passwords(
        self,
        credentials: List[Credential],
        passwords: Optional[List[str]] = None,
    ) -> List[Credential]:
        """
        Detect weak passwords in credentials.
        
        Args:
            credentials: List of credential entities
            passwords: Optional list of plain text passwords
            
        Returns:
            List of credentials with weak passwords
        """
        weak_credentials = []
        
        for i, credential in enumerate(credentials):
            password = passwords[i] if passwords and i < len(passwords) else None
            
            if password:
                analysis = self.risk_analyzer.analyze_credential(password)
                if analysis["is_weak"] or analysis["risk_level"] == "HIGH":
                    weak_credentials.append(credential)
        
        return weak_credentials
    
    async def update_credential_with_analysis(
        self,
        credential: Credential,
        password: Optional[str],
        credential_repository: CredentialRepository,
    ) -> Credential:
        """
        Analyze credential and update it with analysis results.
        
        Args:
            credential: Credential entity
            password: Optional plain text password
            credential_repository: Credential repository
            
        Returns:
            Updated credential
        """
        if not password:
            return credential
        
        # Analyze
        analysis = self.risk_analyzer.analyze_credential(
            password=password,
            email=credential.email,
        )
        
        # Update credential
        credential.password_strength_score = int(100 - analysis["risk_score"])
        credential.risk_score = analysis["risk_score"] / 10.0  # Convert to 0-10 scale
        credential.is_weak = analysis["is_weak"]
        credential.recommendations = analysis["recommendations"]
        credential.ml_features = analysis["features"]
        
        # Determine pattern type
        features = analysis["features"]
        if features.get("is_common", 0) > 0:
            credential.pattern_type = "common"
        elif features.get("contains_dictionary_word", 0) > 0:
            credential.pattern_type = "dictionary"
        elif features.get("has_sequential", 0) > 0:
            credential.pattern_type = "sequential"
        elif features.get("repeated_chars", 0) > 0:
            credential.pattern_type = "repeated"
        else:
            credential.pattern_type = "random"
        
        # Save updated credential
        updated = await credential_repository.update(credential)
        
        return updated
