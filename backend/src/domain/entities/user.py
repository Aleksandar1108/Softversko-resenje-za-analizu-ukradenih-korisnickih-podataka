"""User entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class User:
    """User entity."""
    
    id: Optional[UUID]
    email: str
    password_hash: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    email_verified: bool
    notification_preferences: dict
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    
    def __post_init__(self):
        """Validate user data."""
        if not self.email:
            raise ValueError("Email is required")
        if not self.password_hash:
            raise ValueError("Password hash is required")
