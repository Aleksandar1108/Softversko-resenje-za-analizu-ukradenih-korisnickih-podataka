"""Create SQLite database."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.database.database import async_engine
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.breach_model import BreachModel
from src.infrastructure.database.models.credential_model import CredentialModel
from src.infrastructure.database.models.user_model import UserModel


async def main():
    """Create database tables."""
    print("Creating SQLite database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database created successfully!")
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
