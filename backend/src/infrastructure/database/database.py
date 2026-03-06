"""Database connection and setup."""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ...config.settings import settings


# Create async engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency for getting database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database (create tables)."""
    from sqlalchemy.ext.asyncio import AsyncSession
    
    async with async_engine.begin() as conn:
        # Import all models to register them
        from .models import breach_model, credential_model, user_model
        
        # Create all tables
        await conn.run_sync(lambda sync_conn: sync_conn.execute(
            "CREATE EXTENSION IF NOT EXISTS 'uuid-ossp'"
        ))
        await conn.run_sync(lambda sync_conn: sync_conn.execute(
            "CREATE TABLE IF NOT EXISTS breaches (...)"
        ))
