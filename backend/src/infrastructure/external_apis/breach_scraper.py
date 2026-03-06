"""Web scraper for breach data."""
import asyncio
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from bs4 import BeautifulSoup
import httpx

from ...domain.entities.breach import Breach


class BreachScraper:
    """Web scraper for collecting breach data from public sources."""
    
    # Default sources (these are examples - adjust based on actual available sources)
    DEFAULT_SOURCES = [
        # Add actual breach database URLs here
        # Note: Only scrape from sources that allow it and respect robots.txt
    ]
    
    # Email regex pattern
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    def __init__(self):
        """Initialize breach scraper."""
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            },
            follow_redirects=True,
        )
    
    async def scrape_breaches(self, sources: List[str] = None) -> List[Breach]:
        """
        Scrape breach data from specified sources.
        
        Args:
            sources: List of URLs to scrape. If None, uses default sources.
            
        Returns:
            List of scraped breach entities
        """
        if sources is None:
            sources = self.DEFAULT_SOURCES
        
        if not sources:
            return []
        
        # Scrape sources in parallel
        tasks = [self._scrape_source(source_url) for source_url in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_breaches = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error in scraping task: {result}")
                continue
            all_breaches.extend(result)
        
        return all_breaches
    
    async def _scrape_source(self, url: str) -> List[Breach]:
        """
        Scrape breaches from a specific source.
        
        Args:
            url: Source URL
            
        Returns:
            List of breach entities
        """
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            breaches = []
            
            # Try different parsing strategies based on common breach database structures
            # Strategy 1: Look for breach entries in tables
            tables = soup.find_all("table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows[1:]:  # Skip header
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        breach = self._parse_table_row(cells, url)
                        if breach:
                            breaches.append(breach)
            
            # Strategy 2: Look for breach entries in divs/cards
            breach_cards = soup.find_all(["div", "article"], class_=re.compile(r"breach|leak|data", re.I))
            for card in breach_cards:
                breach = self._parse_breach_card(card, url)
                if breach:
                    breaches.append(breach)
            
            # Strategy 3: Look for structured data (JSON-LD)
            json_scripts = soup.find_all("script", type="application/ld+json")
            for script in json_scripts:
                try:
                    import json
                    data = json.loads(script.string)
                    breach = self._parse_json_ld(data, url)
                    if breach:
                        breaches.append(breach)
                except:
                    pass
            
            # Strategy 4: Generic parsing - look for breach-like patterns
            if not breaches:
                breach = self._parse_generic(soup, url)
                if breach:
                    breaches.append(breach)
            
            return breaches
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP error scraping {url}: {e}")
            return []
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    def _parse_table_row(self, cells, source_url: str) -> Optional[Breach]:
        """Parse breach data from table row."""
        try:
            if len(cells) < 2:
                return None
            
            name = cells[0].get_text(strip=True)
            if not name or len(name) < 2:
                return None
            
            # Try to extract additional info
            domain = None
            date_str = None
            count_str = None
            
            for i, cell in enumerate(cells[1:], 1):
                text = cell.get_text(strip=True)
                # Try to identify domain
                if '.' in text and '@' not in text and len(text) < 50:
                    domain = text
                # Try to identify date
                if re.match(r'\d{4}-\d{2}-\d{2}', text):
                    date_str = text
                # Try to identify count
                if text.isdigit() and len(text) < 10:
                    count_str = text
            
            return self._create_breach_entity(
                name=name,
                domain=domain,
                date_str=date_str,
                count_str=count_str,
                source_url=source_url,
            )
        except Exception:
            return None
    
    def _parse_breach_card(self, card, source_url: str) -> Optional[Breach]:
        """Parse breach data from card/div element."""
        try:
            # Look for title/name
            title_elem = card.find(["h1", "h2", "h3", "h4", "span", "div"], class_=re.compile(r"title|name|breach", re.I))
            if not title_elem:
                title_elem = card.find(["h1", "h2", "h3"])
            
            name = title_elem.get_text(strip=True) if title_elem else None
            if not name:
                return None
            
            # Look for domain
            domain_elem = card.find(string=re.compile(r'\.(com|org|net|edu)', re.I))
            domain = domain_elem.strip() if domain_elem else None
            
            # Look for date
            date_elem = card.find(string=re.compile(r'\d{4}-\d{2}-\d{2}'))
            date_str = date_elem.strip() if date_elem else None
            
            # Look for count
            count_elem = card.find(string=re.compile(r'\d+.*(record|account|user)', re.I))
            count_str = None
            if count_elem:
                match = re.search(r'(\d+)', count_elem)
                if match:
                    count_str = match.group(1)
            
            return self._create_breach_entity(
                name=name,
                domain=domain,
                date_str=date_str,
                count_str=count_str,
                source_url=source_url,
            )
        except Exception:
            return None
    
    def _parse_json_ld(self, data: dict, source_url: str) -> Optional[Breach]:
        """Parse breach data from JSON-LD structured data."""
        try:
            if isinstance(data, list):
                data = data[0] if data else {}
            
            name = data.get("name") or data.get("headline")
            if not name:
                return None
            
            domain = data.get("url") or data.get("domain")
            date_str = data.get("datePublished") or data.get("dateCreated")
            
            return self._create_breach_entity(
                name=name,
                domain=domain,
                date_str=date_str,
                count_str=None,
                source_url=source_url,
            )
        except Exception:
            return None
    
    def _parse_generic(self, soup, source_url: str) -> Optional[Breach]:
        """Generic parsing fallback."""
        try:
            # Try to get title
            title = soup.find("title")
            if title:
                name = title.get_text(strip=True)
                # Extract domain from URL
                domain = None
                if source_url:
                    match = re.search(r'https?://([^/]+)', source_url)
                    if match:
                        domain = match.group(1)
                
                return self._create_breach_entity(
                    name=name,
                    domain=domain,
                    date_str=None,
                    count_str=None,
                    source_url=source_url,
                )
        except Exception:
            pass
        
        return None
    
    def _create_breach_entity(
        self,
        name: str,
        domain: Optional[str],
        date_str: Optional[str],
        count_str: Optional[str],
        source_url: str,
    ) -> Breach:
        """Create breach entity from parsed data."""
        # Parse date
        breach_date = None
        if date_str:
            try:
                # Try different date formats
                for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        breach_date = datetime.strptime(date_str[:10], fmt).date()
                        break
                    except ValueError:
                        continue
            except Exception:
                pass
        
        # Parse count
        pwn_count = None
        if count_str:
            try:
                pwn_count = int(count_str.replace(',', '').replace('.', ''))
            except ValueError:
                pass
        
        return Breach(
            id=uuid4(),
            name=name[:255],  # Limit length
            domain=domain[:255] if domain else None,
            breach_date=breach_date,
            added_date=datetime.utcnow(),
            modified_date=None,
            pwn_count=pwn_count,
            description=None,
            data_classes=[],
            is_verified=False,
            is_fabricated=False,
            is_sensitive=False,
            is_retired=False,
            is_spam_list=False,
            logo_path=None,
            source="scraped",
            metadata={
                "source_url": source_url,
            },
        )
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
