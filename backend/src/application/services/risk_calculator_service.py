"""Service for calculating risk scores."""
from datetime import datetime, timedelta

from ....domain.entities.credential import Credential
from ....domain.value_objects.risk_score import RiskLevel, RiskScore


class RiskCalculatorService:
    """Service for calculating risk scores for credentials."""
    
    def __init__(self):
        """Initialize risk calculator service."""
        pass
    
    async def calculate_risk(self, credential: Credential) -> RiskScore:
        """
        Calculate risk score for a credential.
        
        Args:
            credential: Credential entity to assess
            
        Returns:
            RiskScore value object
        """
        risk_value = 0.0
        factors = []
        
        # Factor 1: Password strength (0-3.0)
        if credential.is_weak:
            risk_value += 3.0
            factors.append("Weak password detected")
        elif credential.password_strength_score:
            if credential.password_strength_score < 30:
                risk_value += 3.0
                factors.append("Very weak password")
            elif credential.password_strength_score < 60:
                risk_value += 1.5
                factors.append("Medium strength password")
        
        # Factor 2: Pattern type (0-2.0)
        if credential.pattern_type == "common":
            risk_value += 2.0
            factors.append("Common password pattern")
        elif credential.pattern_type == "dictionary":
            risk_value += 1.5
            factors.append("Dictionary word pattern")
        elif credential.pattern_type == "sequential":
            risk_value += 1.0
            factors.append("Sequential pattern")
        
        # Factor 3: Breach age (0-2.0)
        if credential.discovered_date:
            days_old = (datetime.utcnow() - credential.discovered_date).days
            if days_old > 365:
                risk_value += 2.0
                factors.append("Old breach (more than 1 year)")
            elif days_old > 180:
                risk_value += 1.0
                factors.append("Moderately old breach")
        
        # Factor 4: Multiple breaches (0-2.0)
        # This would require checking other credentials with same email
        # For now, we'll use a placeholder
        
        # Factor 5: Sensitive data classes (0-1.0)
        # This would require breach information
        # Placeholder for now
        
        # Normalize to 0.0-10.0
        risk_value = min(10.0, max(0.0, risk_value))
        
        # Determine level
        if risk_value < 3.0:
            level = RiskLevel.LOW
        elif risk_value < 6.0:
            level = RiskLevel.MEDIUM
        elif risk_value < 8.0:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL
        
        return RiskScore(
            value=risk_value,
            level=level,
            factors=factors,
        )
