"""HaveIBeenPwned API client."""
import hashlib
from datetime import date, datetime
from typing import List, Optional
from urllib.parse import quote

import httpx

from src.config.settings import settings
from src.domain.entities.breach import Breach


class HIBPClient:
    """Client for HaveIBeenPwned API."""
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize HIBP client."""
        self.api_key = api_key or settings.HIBP_API_KEY
        # Remove empty strings - treat as None
        if self.api_key == "":
            self.api_key = None
        
        # Base headers
        base_headers = {"User-Agent": "BreachAnalyzer/1.0"}
        
        # Add API key if available
        if self.api_key:
            base_headers["hibp-api-key"] = self.api_key
            print(f"HIBP Client initialized with API key: {self.api_key[:8]}...")
        else:
            print("HIBP Client initialized WITHOUT API key (rate limited)")
        
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=base_headers
        )
    
    async def get_breaches_for_email(self, email: str) -> List[Breach]:
        """
        Get all breaches for an email address.
        
        Args:
            email: Email address to check
            
        Returns:
            List of breach entities
        """
        # URL encode email address
        encoded_email = quote(email, safe='')
        url = f"{self.BASE_URL}/breachedaccount/{encoded_email}"
        
        print(f"HIBP: Checking email {email} (encoded: {encoded_email})")
        print(f"HIBP: URL: {url}")
        print(f"HIBP: Has API key: {bool(self.api_key)}")
        
        try:
            # Use client with headers already set in __init__
            response = await self.client.get(
                url, 
                params={"truncateResponse": "false"}
            )
            
            if response.status_code == 404:
                # Email not found in any breach
                print(f"HIBP: Email {email} not found in any breach")
                return []
            
            if response.status_code == 401:
                # API key required or invalid
                error_text = response.text
                print(f"HIBP API 401 error: {error_text}")
                print("HIBP API key required or invalid. Add valid HIBP_API_KEY to .env file.")
                print("Get your free API key at: https://haveibeenpwned.com/API/Key")
                # Try without API key using rate-limited endpoint
                print("⚠️ HIBP API key nije dodat. Email provera neće raditi bez API key-a.")
                print("💡 HIBP API key je BESPLATAN! Dobijte ga na: https://haveibeenpwned.com/API/Key")
                print("💡 Alternativa: Koristite Password Check (besplatno, bez API key-a)")
                return await self._get_breaches_without_key(email)
            
            if response.status_code == 429:
                # Rate limit exceeded
                print("HIBP API rate limit exceeded. Please wait or add API key.")
                return []
            
            response.raise_for_status()
            breaches_data = response.json()
            
            if not isinstance(breaches_data, list):
                print(f"HIBP API returned unexpected format: {type(breaches_data)}")
                return []
            
            # Convert to domain entities
            breaches = []
            for breach_data in breaches_data:
                try:
                    breach = self._parse_breach_data(breach_data)
                    breaches.append(breach)
                except Exception as parse_error:
                    print(f"Error parsing breach data: {parse_error}")
                    continue
            
            print(f"HIBP: Found {len(breaches)} breaches for {email}")
            return breaches
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"HIBP: Email {email} not found in any breach")
                return []
            if e.response.status_code == 401:
                print(f"HIBP API 401: {e.response.text}")
                print("HIBP API key required. Get free key at: https://haveibeenpwned.com/API/Key")
                return await self._get_breaches_without_key(email)
            if e.response.status_code == 429:
                print("HIBP API rate limit exceeded")
                return []
            # Other HTTP error
            print(f"HIBP API HTTP error {e.response.status_code}: {e.response.text}")
            return []
        except httpx.RequestError as e:
            # Network error
            print(f"HIBP API network error: {e}")
            return []
        except Exception as e:
            # Any other error
            print(f"HIBP API error: {e}")
            import traceback
            print(traceback.format_exc())
            return []
    
    async def _get_breaches_without_key(self, email: str) -> List[Breach]:
        """
        Fallback method: Try to get breach names without API key (rate limited).
        This uses the public endpoint which has strict rate limits.
        """
        try:
            # Use the public endpoint (no API key, but rate limited)
            encoded_email = quote(email, safe='')
            url = f"{self.BASE_URL}/breachedaccount/{encoded_email}"
            
            # Create a client without API key for public access
            public_client = httpx.AsyncClient(
                timeout=30.0,
                headers={"User-Agent": "BreachAnalyzer/1.0"}
            )
            
            try:
                response = await public_client.get(url, params={"truncateResponse": "false"})
                
                if response.status_code == 404:
                    return []
                
                if response.status_code == 429:
                    print("HIBP rate limit: Too many requests. Please add API key or wait.")
                    return []
                
                response.raise_for_status()
                breaches_data = response.json()
                
                if not isinstance(breaches_data, list):
                    return []
                
                breaches = []
                for breach_data in breaches_data:
                    try:
                        breach = self._parse_breach_data(breach_data)
                        breaches.append(breach)
                    except Exception:
                        continue
                
                print(f"HIBP (public): Found {len(breaches)} breaches for {email}")
                return breaches
            finally:
                await public_client.aclose()
        except Exception as e:
            print(f"Error in fallback HIBP check: {e}")
            return []
    
    async def check_password_breached(self, password: str) -> dict:
        """
        Check if password has been breached using HIBP Password API (k-anonymity).
        
        This uses the k-anonymity model - only first 5 chars of SHA-1 hash are sent.
        API returns all hashes that start with those 5 chars, then we check locally.
        
        Args:
            password: Plain text password to check
            
        Returns:
            Dictionary with:
            - is_breached: bool
            - count: int (number of times password was found in breaches)
            - message: str
        """
        try:
            # Calculate SHA-1 hash
            password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            
            # Get first 5 characters (k-anonymity)
            hash_prefix = password_hash[:5]
            hash_suffix = password_hash[5:]
            
            # Call HIBP Password API
            url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
            
            print(f"HIBP Password: Checking password (hash prefix: {hash_prefix}...)")
            
            # Use separate client for password API (different domain)
            password_client = httpx.AsyncClient(
                timeout=30.0,
                headers={"User-Agent": "BreachAnalyzer/1.0"}
            )
            
            try:
                response = await password_client.get(url)
                response.raise_for_status()
                
                # Response is text with format: HASH_SUFFIX:COUNT
                # Example: 0018A45C4D1DEF81644B54AB7F969B88D65:1
                response_text = response.text
                
                # Check if our hash suffix is in the response
                count = 0
                for line in response_text.strip().split('\n'):
                    if ':' in line:
                        suffix, breach_count = line.split(':', 1)
                        if suffix == hash_suffix:
                            count = int(breach_count.strip())
                            break
                
                is_breached = count > 0
                
                if is_breached:
                    message = f"Password has been found in {count:,} data breaches!"
                else:
                    message = "Password has not been found in any known data breaches."
                
                print(f"HIBP Password: {'BREACHED' if is_breached else 'SAFE'} (count: {count})")
                
                return {
                    "is_breached": is_breached,
                    "count": count,
                    "message": message,
                    "hash_prefix": hash_prefix,  # For debugging
                }
                
            finally:
                await password_client.aclose()
                
        except httpx.HTTPStatusError as e:
            print(f"HIBP Password API HTTP error: {e.response.status_code}")
            return {
                "is_breached": False,
                "count": 0,
                "message": "Unable to check password (API error).",
            }
        except httpx.RequestError as e:
            print(f"HIBP Password API network error: {e}")
            return {
                "is_breached": False,
                "count": 0,
                "message": "Unable to check password (network error).",
            }
        except Exception as e:
            print(f"HIBP Password API error: {e}")
            import traceback
            print(traceback.format_exc())
            return {
                "is_breached": False,
                "count": 0,
                "message": "Unable to check password (unknown error).",
            }
    
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
        except httpx.HTTPStatusError as e:
            print(f"HIBP API HTTP error: {e.response.status_code} - {e.response.text}")
            return []
        except httpx.RequestError as e:
            print(f"HIBP API network error: {e}")
            return []
        except Exception as e:
            print(f"HIBP API error: {e}")
            return []
    
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
            print(f"HIBP API HTTP error: {e.response.status_code}")
            return None
        except Exception as e:
            print(f"HIBP API error: {e}")
            return None
    
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
