"""Data collection use cases."""
from .collect_hibp_data import CollectHIBPDataUseCase
from .scrape_breach_data import ScrapeBreachDataUseCase

__all__ = [
    "CollectHIBPDataUseCase",
    "ScrapeBreachDataUseCase",
]
