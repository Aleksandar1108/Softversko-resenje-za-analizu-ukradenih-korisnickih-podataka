"""User API schemas."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    email_verified: bool
    notification_preferences: dict
    created_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


class EmailCheckRequest(BaseModel):
    """Schema for email check request."""
    email: EmailStr


class EmailCheckResponse(BaseModel):
    """Schema for email check response."""
    email: str
    is_breached: bool
    total_breaches: int
    breaches: List[dict]
    statistics: dict
