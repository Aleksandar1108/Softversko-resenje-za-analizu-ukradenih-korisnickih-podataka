"""Credential entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class Credential:
    """Credential entity representing compromised credentials."""
    
    id: Optional[UUID]
    email: str
    password_hash: Optional[str]  # SHA-1 hash
    breach_id: UUID
    discovered_date: datetime
    password_strength_score: Optional[int]  # 0-100
    risk_score: Optional[float]  # 0.00-10.00
    is_weak: bool
    pattern_type: Optional[str]  # 'common', 'dictionary', 'sequential', etc.
    ml_features: Optional[dict]
    recommendations: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    def __post_init__(self):
        """Validate credential data."""
        if not self.email:
            raise ValueError("Email is required")
        if self.password_strength_score is not None:
            if not 0 <= self.password_strength_score <= 100:
                raise ValueError("Password strength score must be between 0 and 100")
        if self.risk_score is not None:
            if not 0.0 <= self.risk_score <= 10.0:
                raise ValueError("Risk score must be between 0.0 and 10.0")
