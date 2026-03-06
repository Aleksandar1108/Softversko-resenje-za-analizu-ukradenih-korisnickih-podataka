"""Notification queue for async processing."""
from typing import List
from uuid import UUID

from src.domain.entities.notification import Notification
from src.domain.repositories import UserRepository


class NotificationQueue:
    """Queue for managing notifications."""
    
    def __init__(self, user_repository: UserRepository):
        """Initialize notification queue."""
        self.user_repository = user_repository
        self.queue: List[Notification] = []
    
    async def enqueue(self, notification: Notification) -> bool:
        """
        Add notification to queue.
        
        Args:
            notification: Notification entity
            
        Returns:
            True if added successfully
        """
        self.queue.append(notification)
        # In production, this would use a proper queue system (Redis, RabbitMQ, etc.)
        return True
    
    async def dequeue(self) -> Notification:
        """
        Get next notification from queue.
        
        Returns:
            Notification entity or None
        """
        if self.queue:
            return self.queue.pop(0)
        return None
    
    async def get_for_user(self, user_id: UUID) -> List[Notification]:
        """
        Get all notifications for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of notifications
        """
        return [n for n in self.queue if n.user_id == user_id]
    
    async def mark_as_read(self, notification_id: UUID) -> bool:
        """
        Mark notification as read.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            True if marked successfully
        """
        for notification in self.queue:
            if notification.id == notification_id:
                notification.is_read = True
                return True
        return False
