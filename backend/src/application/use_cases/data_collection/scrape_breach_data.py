"""Use case for scraping breach data from web sources."""
from typing import List

from src.domain.entities.breach import Breach
from src.domain.repositories import BreachRepository
from src.infrastructure.external_apis.breach_scraper import BreachScraper


class ScrapeBreachDataUseCase:
    """Use case for scraping breach data from web sources."""
    
    def __init__(
        self,
        breach_scraper: BreachScraper,
        breach_repository: BreachRepository,
    ):
        """Initialize use case with dependencies."""
        self.breach_scraper = breach_scraper
        self.breach_repository = breach_repository
    
    async def execute(self, sources: List[str] = None) -> List[Breach]:
        """
        Scrape breach data from specified sources.
        
        Args:
            sources: List of source URLs to scrape. If None, uses default sources.
            
        Returns:
            List of scraped breaches
        """
        if sources is None:
            sources = []
        
        scraped_breaches = await self.breach_scraper.scrape_breaches(sources)
        
        # Save scraped breaches
        saved_breaches = []
        for breach in scraped_breaches:
            existing_breach = await self.breach_repository.get_by_name(breach.name)
            
            if not existing_breach:
                saved_breach = await self.breach_repository.create(breach)
                saved_breaches.append(saved_breach)
        
        return saved_breaches
