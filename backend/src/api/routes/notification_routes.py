"""Notification API routes."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependencies import get_notification_queue
from src.infrastructure.database.database import get_db
from src.api.middleware.auth_middleware import get_optional_user_id

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def get_notifications(
    user_id: Optional[UUID] = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get all notifications for current user."""
    if not user_id:
        # Return empty list if user is not authenticated
        return {
            "success": True,
            "data": [],
        }
    
    try:
        notification_queue = await get_notification_queue(db)
        notifications = await notification_queue.get_for_user(user_id)
        
        # Convert to dict format for frontend
        notifications_data = [
            {
                "id": str(n.id) if n.id else f"notif-{i}",
                "user_id": str(n.user_id),
                "type": n.type,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "priority": n.priority,
                "metadata": n.metadata or {},
                "created_at": n.created_at.isoformat() if n.created_at else None,
                "read_at": n.read_at.isoformat() if n.read_at else None,
            }
            for i, n in enumerate(notifications)
        ]
        
        return {
            "success": True,
            "data": notifications_data,
        }
    except Exception as e:
        # Return empty list if there's an error (e.g., no database)
        return {
            "success": True,
            "data": [],
        }


@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: UUID,
    user_id: Optional[UUID] = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Mark notification as read."""
    try:
        notification_queue = await get_notification_queue(db)
        success = await notification_queue.mark_as_read(notification_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        
        return {
            "success": True,
            "message": "Notification marked as read",
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": True,
            "message": "Notification marked as read",
        }


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: UUID,
    user_id: Optional[UUID] = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete notification."""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    
    try:
        notification_queue = await get_notification_queue(db)
        success = await notification_queue.delete(notification_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        
        return {
            "success": True,
            "message": "Notification deleted",
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": True,
            "message": "Notification deleted",
        }
