"""Scheduler for automatic data collection."""
import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.config.settings import settings
from src.domain.repositories import BreachRepository, CredentialRepository
from ..external_apis.data_collector_service import DataCollectorService
from ..external_apis.hibp_client import HIBPClient
from ..external_apis.breach_scraper import BreachScraper


logger = logging.getLogger(__name__)


class DataCollectionScheduler:
    """Scheduler for automatic breach data collection."""
    
    def __init__(
        self,
        data_collector: DataCollectorService,
        web_sources: Optional[List[str]] = None,
    ):
        """
        Initialize data collection scheduler.
        
        Args:
            data_collector: Data collector service instance
            web_sources: Optional list of web sources to scrape
        """
        self.data_collector = data_collector
        self.web_sources = web_sources or []
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        """Start the scheduler."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        # Schedule daily HIBP sync (runs at 2 AM daily)
        self.scheduler.add_job(
            self._sync_hibp_breaches,
            trigger=CronTrigger(hour=2, minute=0),
            id="sync_hibp_daily",
            name="Sync HIBP breaches daily",
            replace_existing=True,
        )
        
        # Schedule weekly web scraping (runs every Sunday at 3 AM)
        if self.web_sources:
            self.scheduler.add_job(
                self._scrape_web_sources,
                trigger=CronTrigger(day_of_week="sun", hour=3, minute=0),
                id="scrape_web_weekly",
                name="Scrape web sources weekly",
                replace_existing=True,
            )
        
        # Schedule periodic credential collection (every 6 hours)
        self.scheduler.add_job(
            self._collect_credentials,
            trigger=IntervalTrigger(hours=6),
            id="collect_credentials_periodic",
            name="Collect credentials periodically",
            replace_existing=True,
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("Data collection scheduler started")
    
    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("Data collection scheduler stopped")
    
    async def _sync_hibp_breaches(self):
        """Synchronize breaches from HIBP API."""
        logger.info("Starting HIBP breach synchronization...")
        
        try:
            stats = await self.data_collector.collect_from_hibp()
            logger.info(
                f"HIBP sync completed: "
                f"{stats['breaches_collected']} breaches collected, "
                f"{stats['duplicates_skipped']} duplicates skipped"
            )
        except Exception as e:
            logger.error(f"Error in HIBP sync: {e}", exc_info=True)
    
    async def _scrape_web_sources(self):
        """Scrape breach data from web sources."""
        logger.info(f"Starting web scraping from {len(self.web_sources)} sources...")
        
        try:
            stats = await self.data_collector.collect_from_web_scraping(
                self.web_sources,
                parse_credentials=True,
            )
            logger.info(
                f"Web scraping completed: "
                f"{stats['breaches_collected']} breaches collected, "
                f"{stats['credentials_collected']} credentials collected, "
                f"{stats['duplicates_skipped']} duplicates skipped, "
                f"{stats['errors']} errors"
            )
        except Exception as e:
            logger.error(f"Error in web scraping: {e}", exc_info=True)
    
    async def _collect_credentials(self):
        """Periodic credential collection."""
        logger.info("Starting periodic credential collection...")
        
        try:
            # Collect from all sources
            stats = await self.data_collector.collect_all(self.web_sources)
            logger.info(
                f"Credential collection completed: "
                f"{stats['breaches_collected']} breaches, "
                f"{stats['credentials_collected']} credentials, "
                f"{stats['duplicates_skipped']} duplicates skipped"
            )
        except Exception as e:
            logger.error(f"Error in credential collection: {e}", exc_info=True)
    
    def add_manual_job(
        self,
        job_func,
        trigger,
        job_id: str,
        name: str = None,
    ):
        """
        Add a manual job to the scheduler.
        
        Args:
            job_func: Async function to execute
            trigger: APScheduler trigger
            job_id: Unique job identifier
            name: Job name
        """
        self.scheduler.add_job(
            job_func,
            trigger=trigger,
            id=job_id,
            name=name or job_id,
            replace_existing=True,
        )
    
    def remove_job(self, job_id: str):
        """Remove a job from the scheduler."""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job {job_id} removed")
        except Exception as e:
            logger.warning(f"Error removing job {job_id}: {e}")


async def create_scheduler(
    breach_repository: BreachRepository,
    credential_repository: CredentialRepository,
    web_sources: Optional[List[str]] = None,
) -> DataCollectionScheduler:
    """
    Factory function to create and configure scheduler.
    
    Args:
        breach_repository: Breach repository instance
        credential_repository: Credential repository instance
        web_sources: Optional list of web sources to scrape
        
    Returns:
        Configured scheduler instance
    """
    hibp_client = HIBPClient()
    breach_scraper = BreachScraper()
    
    data_collector = DataCollectorService(
        hibp_client=hibp_client,
        breach_scraper=breach_scraper,
        breach_repository=breach_repository,
        credential_repository=credential_repository,
    )
    
    scheduler = DataCollectionScheduler(
        data_collector=data_collector,
        web_sources=web_sources,
    )
    
    return scheduler
