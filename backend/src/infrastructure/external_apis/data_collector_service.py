"""Service for collecting breach data from multiple sources."""
import asyncio
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from uuid import uuid4

import httpx
from bs4 import BeautifulSoup

from src.domain.entities.breach import Breach
from src.domain.entities.credential import Credential
from src.domain.repositories import BreachRepository, CredentialRepository
from .hibp_client import HIBPClient
from .breach_scraper import BreachScraper


class DataCollectorService:
    """Service for collecting and normalizing breach data."""
    
    # Email regex pattern
    EMAIL_PATTERN = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # Common password patterns to identify
    PASSWORD_INDICATORS = [
        r'password[:\s=]+([^\s\n]+)',
        r'pass[:\s=]+([^\s\n]+)',
        r'pwd[:\s=]+([^\s\n]+)',
    ]
    
    def __init__(
        self,
        hibp_client: HIBPClient,
        breach_scraper: BreachScraper,
        breach_repository: BreachRepository,
        credential_repository: CredentialRepository,
    ):
        """Initialize data collector service."""
        self.hibp_client = hibp_client
        self.breach_scraper = breach_scraper
        self.breach_repository = breach_repository
        self.credential_repository = credential_repository
        self.seen_credentials: Set[str] = set()  # Track seen credentials to avoid duplicates
    
    async def collect_from_hibp(self, email: Optional[str] = None) -> Dict[str, int]:
        """
        Collect breach data from HaveIBeenPwned API.
        
        Args:
            email: Optional email to check. If None, syncs all breaches.
            
        Returns:
            Dictionary with collection statistics
        """
        stats = {
            "breaches_collected": 0,
            "credentials_collected": 0,
            "duplicates_skipped": 0,
        }
        
        try:
            if email:
                # Collect breaches for specific email
                breaches = await self.hibp_client.get_breaches_for_email(email)
            else:
                # Sync all breaches
                breaches = await self.hibp_client.get_all_breaches()
            
            for breach in breaches:
                # Check for duplicates
                existing_breach = await self.breach_repository.get_by_name(breach.name)
                
                if existing_breach:
                    # Update existing breach if needed
                    if existing_breach.modified_date != breach.modified_date:
                        breach.id = existing_breach.id
                        await self.breach_repository.update(breach)
                    stats["duplicates_skipped"] += 1
                else:
                    # Save new breach
                    saved_breach = await self.breach_repository.create(breach)
                    stats["breaches_collected"] += 1
                    
                    # Note: HIBP API doesn't provide actual credentials,
                    # only breach metadata. Credentials would come from other sources.
            
        except Exception as e:
            print(f"Error collecting from HIBP: {e}")
        
        return stats
    
    async def collect_from_web_scraping(
        self,
        sources: List[str],
        parse_credentials: bool = True,
    ) -> Dict[str, int]:
        """
        Collect breach data from web scraping.
        
        Args:
            sources: List of URLs to scrape
            parse_credentials: Whether to parse email/password data
            
        Returns:
            Dictionary with collection statistics
        """
        stats = {
            "breaches_collected": 0,
            "credentials_collected": 0,
            "duplicates_skipped": 0,
            "errors": 0,
        }
        
        for source_url in sources:
            try:
                # Scrape breaches
                breaches = await self.breach_scraper.scrape_breaches([source_url])
                
                for breach in breaches:
                    # Check for duplicates
                    existing_breach = await self.breach_repository.get_by_name(breach.name)
                    
                    if existing_breach:
                        breach.id = existing_breach.id
                        stats["duplicates_skipped"] += 1
                    else:
                        saved_breach = await self.breach_repository.create(breach)
                        stats["breaches_collected"] += 1
                    
                    # If parsing credentials, extract them from the source
                    if parse_credentials and existing_breach:
                        breach = existing_breach
                    
                    if parse_credentials:
                        credentials = await self._extract_credentials_from_source(
                            source_url, breach
                        )
                        
                        for credential in credentials:
                            if await self._save_credential_if_new(credential):
                                stats["credentials_collected"] += 1
                            else:
                                stats["duplicates_skipped"] += 1
                        
            except Exception as e:
                print(f"Error scraping {source_url}: {e}")
                stats["errors"] += 1
        
        return stats
    
    async def _extract_credentials_from_source(
        self,
        source_url: str,
        breach: Breach,
    ) -> List[Credential]:
        """
        Extract credentials from a source URL.
        
        Args:
            source_url: URL to extract from
            breach: Associated breach entity
            
        Returns:
            List of extracted credentials
        """
        credentials = []
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(source_url)
                response.raise_for_status()
                
                # Parse text content
                text = response.text
                
                # Extract email-password pairs
                email_password_pairs = self._parse_credentials(text)
                
                for email, password in email_password_pairs:
                    # Normalize email
                    normalized_email = self._normalize_email(email)
                    if not normalized_email:
                        continue
                    
                    # Hash password (SHA-1 for HIBP compatibility)
                    password_hash = hashlib.sha1(password.encode()).hexdigest().upper()
                    
                    # Create credential entity
                    credential = Credential(
                        id=uuid4(),
                        email=normalized_email,
                        password_hash=password_hash,
                        breach_id=breach.id,
                        discovered_date=datetime.utcnow(),
                        password_strength_score=None,
                        risk_score=None,
                        is_weak=False,
                        pattern_type=None,
                        ml_features=None,
                        recommendations=[],
                        created_at=datetime.utcnow(),
                        updated_at=None,
                    )
                    
                    credentials.append(credential)
        
        except Exception as e:
            print(f"Error extracting credentials from {source_url}: {e}")
        
        return credentials
    
    def _parse_credentials(self, text: str) -> List[Tuple[str, str]]:
        """
        Parse email-password pairs from text.
        
        Args:
            text: Text content to parse
            
        Returns:
            List of (email, password) tuples
        """
        pairs = []
        
        # Find all emails
        emails = self.EMAIL_PATTERN.findall(text)
        
        # Try to find associated passwords
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Look for email in line
            email_match = self.EMAIL_PATTERN.search(line)
            if not email_match:
                continue
            
            email = email_match.group(0)
            
            # Look for password in same line or next few lines
            password = None
            
            # Check current line for password patterns
            for pattern in self.PASSWORD_INDICATORS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    password = match.group(1).strip()
                    break
            
            # If not found, check next lines (common formats: email:password, email|password)
            if not password:
                # Check for colon or pipe separator
                parts = re.split(r'[:|;]', line)
                if len(parts) >= 2:
                    potential_password = parts[1].strip()
                    if len(potential_password) > 0 and len(potential_password) < 200:
                        password = potential_password
                
                # Check next line
                if not password and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if len(next_line) > 0 and len(next_line) < 200:
                        # Basic validation: not another email
                        if '@' not in next_line:
                            password = next_line
            
            if password:
                # Basic password validation
                if 4 <= len(password) <= 200 and not password.startswith('http'):
                    pairs.append((email, password))
        
        return pairs
    
    def _normalize_email(self, email: str) -> Optional[str]:
        """
        Normalize email address.
        
        Args:
            email: Email to normalize
            
        Returns:
            Normalized email or None if invalid
        """
        if not email:
            return None
        
        # Convert to lowercase
        email = email.lower().strip()
        
        # Remove whitespace
        email = email.replace(' ', '').replace('\t', '')
        
        # Validate email format
        if not self.EMAIL_PATTERN.match(email):
            return None
        
        # Remove common prefixes/suffixes
        email = email.replace('mailto:', '')
        
        return email
    
    def _normalize_password(self, password: str) -> Optional[str]:
        """
        Normalize password.
        
        Args:
            password: Password to normalize
            
        Returns:
            Normalized password or None if invalid
        """
        if not password:
            return None
        
        # Remove whitespace
        password = password.strip()
        
        # Basic validation
        if len(password) < 4 or len(password) > 200:
            return None
        
        # Remove common prefixes
        password = password.replace('password:', '').replace('pass:', '')
        password = password.strip()
        
        return password if password else None
    
    async def _save_credential_if_new(self, credential: Credential) -> bool:
        """
        Save credential if it's new (not a duplicate).
        
        Args:
            credential: Credential to save
            
        Returns:
            True if credential was saved, False if duplicate
        """
        # Create unique key for duplicate detection
        credential_key = f"{credential.email}:{credential.password_hash}:{credential.breach_id}"
        
        if credential_key in self.seen_credentials:
            return False
        
        # Check database for existing credential
        existing_credentials = await self.credential_repository.get_by_email(credential.email)
        
        for existing in existing_credentials:
            if (
                existing.password_hash == credential.password_hash
                and existing.breach_id == credential.breach_id
            ):
                # Duplicate found
                self.seen_credentials.add(credential_key)
                return False
        
        # Save new credential
        try:
            await self.credential_repository.create(credential)
            self.seen_credentials.add(credential_key)
            return True
        except Exception as e:
            print(f"Error saving credential: {e}")
            return False
    
    async def collect_all(self, sources: List[str] = None) -> Dict[str, int]:
        """
        Collect data from all sources.
        
        Args:
            sources: Optional list of web sources to scrape
            
        Returns:
            Combined statistics
        """
        stats = {
            "breaches_collected": 0,
            "credentials_collected": 0,
            "duplicates_skipped": 0,
            "errors": 0,
        }
        
        # Collect from HIBP
        try:
            hibp_stats = await self.collect_from_hibp()
            stats["breaches_collected"] += hibp_stats["breaches_collected"]
            stats["duplicates_skipped"] += hibp_stats["duplicates_skipped"]
        except Exception as e:
            print(f"Error in HIBP collection: {e}")
            stats["errors"] += 1
        
        # Collect from web scraping if sources provided
        if sources:
            try:
                scraping_stats = await self.collect_from_web_scraping(sources)
                stats["breaches_collected"] += scraping_stats["breaches_collected"]
                stats["credentials_collected"] += scraping_stats["credentials_collected"]
                stats["duplicates_skipped"] += scraping_stats["duplicates_skipped"]
                stats["errors"] += scraping_stats["errors"]
            except Exception as e:
                print(f"Error in web scraping: {e}")
                stats["errors"] += 1
        
        return stats
