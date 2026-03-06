"""User database model."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, String, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.types import TypeDecorator, CHAR

from .base import Base


# SQLite compatible UUID type
class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, UUID):
                return str(UUID(value))
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, UUID):
                return UUID(value)
            return value


class UserModel(Base):
    """SQLAlchemy model for user table."""
    
    __tablename__ = "users"
    
    id = Column(GUID(), primary_key=True, default=uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    notification_preferences = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
