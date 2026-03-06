"""Breach database model."""
from datetime import date, datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY
from sqlalchemy.orm import relationship

from .base import Base
from .user_model import GUID


class BreachModel(Base):
    """SQLAlchemy model for breach table."""
    
    __tablename__ = "breaches"
    
    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    domain = Column(String(255), nullable=True)
    breach_date = Column(Date, nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_date = Column(DateTime, nullable=True)
    pwn_count = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    data_classes = Column(JSON, nullable=False, default=list)  # JSON for SQLite compatibility
    is_verified = Column(Boolean, default=False, nullable=False)
    is_fabricated = Column(Boolean, default=False, nullable=False)
    is_sensitive = Column(Boolean, default=False, nullable=False)
    is_retired = Column(Boolean, default=False, nullable=False)
    is_spam_list = Column(Boolean, default=False, nullable=False)
    logo_path = Column(String(500), nullable=True)
    source = Column(String(100), nullable=False, default="hibp")
    breach_metadata = Column("metadata", JSON, nullable=True)  # Renamed to avoid SQLAlchemy conflict
    
    # Relationship
    credentials = relationship("CredentialModel", back_populates="breach")
