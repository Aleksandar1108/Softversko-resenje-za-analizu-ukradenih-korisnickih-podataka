"""User-Breach relationship database model."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .user_model import GUID


class UserBreachModel(Base):
    """SQLAlchemy model for user_breaches table."""
    
    __tablename__ = "user_breaches"
    
    id = Column(GUID(), primary_key=True, default=uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False, index=True)
    breach_id = Column(GUID(), ForeignKey("breaches.id"), nullable=False, index=True)
    notified_at = Column(DateTime, nullable=True)
    notification_sent = Column(Boolean, default=False, nullable=False)
    acknowledged_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint to prevent duplicate user-breach pairs
    __table_args__ = (
        UniqueConstraint('user_id', 'breach_id', name='uq_user_breach'),
    )
    
    # Relationships
    user = relationship("UserModel", backref="user_breaches")
    breach = relationship("BreachModel", backref="user_breaches")
