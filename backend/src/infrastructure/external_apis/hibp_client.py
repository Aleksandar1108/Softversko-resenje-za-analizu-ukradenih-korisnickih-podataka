"""HaveIBeenPwned API client."""
import hashlib
from datetime import date, datetime
from typing import List, Optional

import httpx

from ...config.settings import settings
from ...domain.entities.breach import Breach


class HIBPClient:
    """Client for HaveIBeenPwned API."""
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize HIBP client."""
        self.api_key = api_key or settings.HIBP_API_KEY
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "hibp-api-key": self.api_key,
                "User-Agent": "BreachAnalyzer/1.0",
            } if self.api_key else {
                "User-Agent": "BreachAnalyzer/1.0",
            }
        )
    
    async def get_breaches_for_email(self, email: str) -> List[Breach]:
        """
        Get all breaches for an email address.
        
        Args:
            email: Email address to check
            
        Returns:
            List of breach entities
        """
        # Hash email for API call
        email_hash = hashlib.sha1(email.lower().encode()).hexdigest().upper()
        prefix = email_hash[:5]
        suffix = email_hash[5:]
        
        # Use range API for password checking (if needed)
        # For breach checking, use the breachedaccount endpoint
        url = f"{self.BASE_URL}/breachedaccount/{email}"
        
        try:
            response = await self.client.get(url)
            
            if response.status_code == 404:
                # Email not found in any breach
                return []
            
            response.raise_for_status()
            breaches_data = response.json()
            
            # Convert to domain entities
            breaches = []
            for breach_data in breaches_data:
                breach = self._parse_breach_data(breach_data)
                breaches.append(breach)
            
            return breaches
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return []
            raise
        finally:
            await self.client.aclose()
    
    async def get_all_breaches(self) -> List[Breach]:
        """
        Get all available breaches from HIBP.
        
        Returns:
            List of all breach entities
        """
        url = f"{self.BASE_URL}/breaches"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            breaches_data = response.json()
            
            breaches = []
            for breach_data in breaches_data:
                breach = self._parse_breach_data(breach_data)
                breaches.append(breach)
            
            return breaches
            
        finally:
            await self.client.aclose()
    
    async def get_breach_by_name(self, name: str) -> Optional[Breach]:
        """
        Get a specific breach by name.
        
        Args:
            name: Breach name
            
        Returns:
            Breach entity or None
        """
        url = f"{self.BASE_URL}/breach/{name}"
        
        try:
            response = await self.client.get(url)
            
            if response.status_code == 404:
                return None
            
            response.raise_for_status()
            breach_data = response.json()
            
            return self._parse_breach_data(breach_data)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        finally:
            await self.client.aclose()
    
    def _parse_breach_data(self, data: dict) -> Breach:
        """Parse HIBP API response to Breach entity."""
        from uuid import uuid4
        
        # Parse breach date
        breach_date = None
        if data.get("BreachDate"):
            try:
                breach_date = datetime.strptime(data["BreachDate"], "%Y-%m-%d").date()
            except ValueError:
                pass
        
        # Parse added date
        added_date = datetime.utcnow()
        if data.get("AddedDate"):
            try:
                added_date = datetime.fromisoformat(data["AddedDate"].replace("Z", "+00:00"))
            except ValueError:
                pass
        
        # Parse modified date
        modified_date = None
        if data.get("ModifiedDate"):
            try:
                modified_date = datetime.fromisoformat(data["ModifiedDate"].replace("Z", "+00:00"))
            except ValueError:
                pass
        
        return Breach(
            id=uuid4(),
            name=data.get("Name", ""),
            domain=data.get("Domain"),
            breach_date=breach_date,
            added_date=added_date,
            modified_date=modified_date,
            pwn_count=data.get("PwnCount"),
            description=data.get("Description"),
            data_classes=data.get("DataClasses", []),
            is_verified=data.get("IsVerified", False),
            is_fabricated=data.get("IsFabricated", False),
            is_sensitive=data.get("IsSensitive", False),
            is_retired=data.get("IsRetired", False),
            is_spam_list=data.get("IsSpamList", False),
            logo_path=data.get("LogoPath"),
            source="hibp",
            metadata={
                "title": data.get("Title"),
                "is_verified": data.get("IsVerified"),
            },
        )
