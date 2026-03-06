"""Breach API schemas."""
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BreachBase(BaseModel):
    """Base breach schema."""
    name: str
    domain: Optional[str] = None
    breach_date: Optional[date] = None
    pwn_count: Optional[int] = None
    description: Optional[str] = None
    data_classes: List[str] = Field(default_factory=list)
    is_verified: bool = False
    source: str = "hibp"


class BreachCreate(BreachBase):
    """Schema for creating a breach."""
    pass


class BreachResponse(BreachBase):
    """Schema for breach response."""
    id: UUID
    added_date: datetime
    modified_date: Optional[datetime] = None
    is_fabricated: bool = False
    is_sensitive: bool = False
    is_retired: bool = False
    is_spam_list: bool = False
    logo_path: Optional[str] = None
    metadata: Optional[dict] = None
    
    model_config = {"from_attributes": True}


class BreachListResponse(BaseModel):
    """Schema for breach list response."""
    breaches: List[BreachResponse]
    total: int
    skip: int
    limit: int
