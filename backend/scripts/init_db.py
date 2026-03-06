"""Initialize database with tables."""
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.database.database import async_engine, init_db
from src.infrastructure.database.models import breach_model, credential_model, user_model


async def main():
    """Initialize database."""
    print("Initializing database...")
    
    # Import all models to register them
    from src.infrastructure.database.models.base import Base
    
    async with async_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully!")
    
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
