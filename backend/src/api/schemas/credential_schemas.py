"""Credential API schemas."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CredentialBase(BaseModel):
    """Base credential schema."""
    email: str
    password_hash: Optional[str] = None
    breach_id: UUID


class CredentialResponse(CredentialBase):
    """Schema for credential response."""
    id: UUID
    discovered_date: datetime
    password_strength_score: Optional[int] = None
    risk_score: Optional[float] = None
    is_weak: bool = False
    pattern_type: Optional[str] = None
    ml_features: Optional[dict] = None
    recommendations: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class CredentialAnalysisRequest(BaseModel):
    """Schema for credential analysis request."""
    credential_id: UUID


class CredentialAnalysisResponse(BaseModel):
    """Schema for credential analysis response."""
    credential_id: UUID
    password_strength_score: int
    risk_score: float
    is_weak: bool
    pattern_type: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)
