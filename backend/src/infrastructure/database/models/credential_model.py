"""Credential database model."""
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY
from sqlalchemy.orm import relationship

from .base import Base
from .user_model import GUID


class CredentialModel(Base):
    """SQLAlchemy model for credential table."""
    
    __tablename__ = "credentials"
    
    id = Column(GUID(), primary_key=True, default=uuid4)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    breach_id = Column(GUID(), ForeignKey("breaches.id"), nullable=False, index=True)
    discovered_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    password_strength_score = Column(Integer, nullable=True)
    risk_score = Column(Float, nullable=True, index=True)
    is_weak = Column(Boolean, default=False, nullable=False)
    pattern_type = Column(String(50), nullable=True)
    ml_features = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=False, default=list)  # JSON for SQLite compatibility
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationship
    breach = relationship("BreachModel", back_populates="credentials")
