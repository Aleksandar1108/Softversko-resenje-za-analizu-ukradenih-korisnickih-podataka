"""Notification database model."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .user_model import GUID


class NotificationModel(Base):
    """SQLAlchemy model for notification table."""
    
    __tablename__ = "notifications"
    
    id = Column(GUID(), primary_key=True, default=uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # 'breach_alert', 'recommendation', 'trend_update', 'risk_alert'
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    priority = Column(String(20), default="normal", nullable=False)  # 'low', 'normal', 'high', 'critical'
    notification_metadata = Column("metadata", JSON, nullable=True)  # 'metadata' is reserved in SQLAlchemy
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("UserModel", backref="notifications")
