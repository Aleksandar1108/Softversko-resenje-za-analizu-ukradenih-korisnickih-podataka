"""Initialize SQLite database with tables."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.database.database import async_engine
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models import breach_model, credential_model, user_model


async def main():
    """Initialize SQLite database."""
    print("Initializing SQLite database...")
    
    # Import all models to register them with Base
    from src.infrastructure.database.models.breach_model import BreachModel
    from src.infrastructure.database.models.credential_model import CredentialModel
    from src.infrastructure.database.models.user_model import UserModel
    
    async with async_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully!")
    
    await async_engine.dispose()
    print("Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())
