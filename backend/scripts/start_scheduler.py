"""Script to start data collection scheduler."""
import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.infrastructure.database.database import AsyncSessionLocal, init_db
from src.infrastructure.database.repositories import (
    BreachRepositoryImpl,
    CredentialRepositoryImpl,
)
from src.infrastructure.services.data_collection_scheduler import create_scheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start scheduler."""
    logger.info("Initializing data collection scheduler...")
    
    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    
    # Web sources configuration (add your sources here)
    web_sources = [  
        # Example sources (replace with actual breach database URLs)
        # "https://example-breach-db.com/breaches",  
        "https://haveibeenpwned.com/",
    ]
    
    # Create database session
    async with AsyncSessionLocal() as session:
        breach_repo = BreachRepositoryImpl(session)
        credential_repo = CredentialRepositoryImpl(session)
        
        # Create scheduler
        scheduler = await create_scheduler(
            breach_repository=breach_repo,
            credential_repository=credential_repo,
            web_sources=web_sources,
        )
        
        # Start scheduler
        scheduler.start()
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            # Keep running
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.stop()
            logger.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(main())
