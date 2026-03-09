"""Notification queue for async processing."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.notification import Notification
from src.domain.repositories import UserRepository
from src.infrastructure.database.models.notification_model import NotificationModel


class NotificationQueue:
    """Queue for managing notifications with database persistence."""
    
    def __init__(self, user_repository: UserRepository, session: Optional[AsyncSession] = None):
        """Initialize notification queue."""
        self.user_repository = user_repository
        self.session = session
        # Keep in-memory queue for backward compatibility
        self.queue: List[Notification] = []
    
    async def enqueue(self, notification: Notification) -> bool:
        """
        Add notification to queue and save to database.
        
        Args:
            notification: Notification entity
            
        Returns:
            True if added successfully
        """
        # Save to in-memory queue for backward compatibility
        self.queue.append(notification)
        
        # Save to database if session is available
        if self.session:
            try:
                model = NotificationModel(
                    id=notification.id,
                    user_id=notification.user_id,
                    type=notification.type,
                    title=notification.title,
                    message=notification.message,
                    is_read=notification.is_read,
                    priority=notification.priority,
                    notification_metadata=notification.metadata,
                    created_at=notification.created_at,
                    read_at=notification.read_at,
                )
                self.session.add(model)
                await self.session.flush()
                # Update notification ID if it was None
                if not notification.id:
                    notification.id = model.id
                return True
            except Exception as e:
                print(f"Error saving notification to database: {e}")
                # Continue even if database save fails
                return True
        return True
    
    async def dequeue(self) -> Optional[Notification]:
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
        Get all notifications for a user from database.
        
        Args:
            user_id: User ID
            
        Returns:
            List of notifications
        """
        # Try to get from database first
        if self.session:
            try:
                result = await self.session.execute(
                    select(NotificationModel)
                    .where(NotificationModel.user_id == user_id)
                    .order_by(NotificationModel.created_at.desc())
                )
                models = result.scalars().all()
                
                notifications = []
                for model in models:
                    notification = Notification(
                        id=model.id,
                        user_id=model.user_id,
                        type=model.type,
                        title=model.title,
                        message=model.message,
                        is_read=model.is_read,
                        priority=model.priority,
                        metadata=model.notification_metadata,
                        created_at=model.created_at,
                        read_at=model.read_at,
                    )
                    notifications.append(notification)
                
                return notifications
            except Exception as e:
                print(f"Error getting notifications from database: {e}")
                # Fallback to in-memory queue
                pass
        
        # Fallback to in-memory queue
        return [n for n in self.queue if n.user_id == user_id]
    
    async def mark_as_read(self, notification_id: UUID) -> bool:
        """
        Mark notification as read in database.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            True if marked successfully
        """
        # Update in database if session is available
        if self.session:
            try:
                model = await self.session.get(NotificationModel, notification_id)
                if model:
                    model.is_read = True
                    model.read_at = datetime.utcnow()
                    await self.session.flush()
                    return True
            except Exception as e:
                print(f"Error marking notification as read in database: {e}")
                # Fallback to in-memory queue
                pass
        
        # Fallback to in-memory queue
        for notification in self.queue:
            if notification.id == notification_id:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
                return True
        return False
    
    async def delete(self, notification_id: UUID) -> bool:
        """
        Delete notification from database.
        
        Args:
            notification_id: Notification ID
            
        Returns:
            True if deleted successfully
        """
        # Delete from database if session is available
        if self.session:
            try:
                model = await self.session.get(NotificationModel, notification_id)
                if model:
                    await self.session.delete(model)
                    await self.session.flush()
                    return True
            except Exception as e:
                print(f"Error deleting notification from database: {e}")
                # Fallback to in-memory queue
                pass
        
        # Fallback to in-memory queue
        initial_length = len(self.queue)
        self.queue = [n for n in self.queue if n.id != notification_id]
        return len(self.queue) < initial_length