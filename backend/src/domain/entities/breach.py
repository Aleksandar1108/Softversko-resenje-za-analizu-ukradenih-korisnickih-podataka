"""Breach entity."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class Breach:
    """Breach entity representing a data breach."""
    
    id: Optional[UUID]
    name: str
    domain: Optional[str]
    breach_date: Optional[date]
    added_date: datetime
    modified_date: Optional[datetime]
    pwn_count: Optional[int]
    description: Optional[str]
    data_classes: List[str]
    is_verified: bool
    is_fabricated: bool
    is_sensitive: bool
    is_retired: bool
    is_spam_list: bool
    logo_path: Optional[str]
    source: str  # 'hibp', 'scraped', etc.
    metadata: Optional[dict]
    
    def __post_init__(self):
        """Validate breach data."""
        if not self.name:
            raise ValueError("Breach name is required")
        if self.source not in ['hibp', 'scraped', 'manual']:
            raise ValueError(f"Invalid source: {self.source}")
