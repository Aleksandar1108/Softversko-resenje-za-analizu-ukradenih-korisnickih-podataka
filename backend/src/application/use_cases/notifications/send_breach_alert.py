"""Use case for sending breach alerts."""
from typing import List
from uuid import UUID

from ....domain.entities.notification import Notification
from ....domain.entities.user import User
from ....domain.repositories import UserRepository
from ....infrastructure.notifications.email_service import EmailService
from ....infrastructure.notifications.notification_queue import NotificationQueue


class SendBreachAlertUseCase:
    """Use case for sending breach alerts to users."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService,
        notification_queue: NotificationQueue,
    ):
        """Initialize use case with dependencies."""
        self.user_repository = user_repository
        self.email_service = email_service
        self.notification_queue = notification_queue
    
    async def execute(
        self,
        user_id: UUID,
        breach_name: str,
        breach_details: dict,
    ) -> bool:
        """
        Send breach alert to user.
        
        Args:
            user_id: ID of the user
            breach_name: Name of the breach
            breach_details: Additional breach details
            
        Returns:
            True if notification was sent successfully
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Create notification
        notification = Notification(
            id=None,
            user_id=user_id,
            type="breach_alert",
            title=f"New Breach Detected: {breach_name}",
            message=f"Your email was found in the {breach_name} breach. "
                   f"Please change your password immediately.",
            is_read=False,
            priority="high",
            metadata=breach_details,
            created_at=None,
            read_at=None,
        )
        
        # Queue notification
        await self.notification_queue.enqueue(notification)
        
        # Send email if enabled
        if user.notification_preferences.get("email", False):
            await self.email_service.send_breach_alert(
                to_email=user.email,
                breach_name=breach_name,
                breach_details=breach_details,
            )
        
        return True
    
    async def send_batch(self, user_ids: List[UUID], breach_name: str) -> int:
        """
        Send breach alerts to multiple users.
        
        Args:
            user_ids: List of user IDs
            breach_name: Name of the breach
            
        Returns:
            Number of notifications sent
        """
        count = 0
        for user_id in user_ids:
            try:
                await self.execute(user_id, breach_name, {})
                count += 1
            except Exception as e:
                print(f"Error sending alert to user {user_id}: {e}")
        
        return count
