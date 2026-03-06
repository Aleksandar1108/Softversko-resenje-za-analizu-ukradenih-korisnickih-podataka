"""Database connection and setup."""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings


# Create async engine with connection pool settings
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    # SQLite specific settings
    connect_args = {"check_same_thread": False}

async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
    # For SQLite, create tables automatically
    pool_pre_ping=True if "sqlite" not in settings.DATABASE_URL else False,
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
    try:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Database session error: {e}")
                raise  # Re-raise to let FastAPI handle it
            finally:
                await session.close()
    except Exception as e:
        # If database connection fails, log and raise
        print(f"Database connection error: {e}")
        raise  # Re-raise to let FastAPI handle it properly


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
