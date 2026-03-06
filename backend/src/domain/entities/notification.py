"""Notification entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Notification:
    """Notification entity."""
    
    id: Optional[UUID]
    user_id: UUID
    type: str  # 'breach_alert', 'recommendation', 'trend_update'
    title: str
    message: str
    is_read: bool
    priority: str  # 'low', 'normal', 'high', 'critical'
    metadata: Optional[dict]
    created_at: datetime
    read_at: Optional[datetime]
    
    def __post_init__(self):
        """Validate notification data."""
        if not self.title:
            raise ValueError("Notification title is required")
        if not self.message:
            raise ValueError("Notification message is required")
        if self.type not in ['breach_alert', 'recommendation', 'trend_update', 'risk_alert']:
            raise ValueError(f"Invalid notification type: {self.type}")
        if self.priority not in ['low', 'normal', 'high', 'critical']:
            raise ValueError(f"Invalid priority: {self.priority}")
