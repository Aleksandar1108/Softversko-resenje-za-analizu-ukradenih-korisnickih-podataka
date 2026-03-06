"""External API clients."""
from .breach_scraper import BreachScraper
from .data_collector_service import DataCollectorService
from .hibp_client import HIBPClient

__all__ = [
    "HIBPClient",
    "BreachScraper",
    "DataCollectorService",
]
