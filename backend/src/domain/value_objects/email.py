"""Email value object."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Email value object with validation."""
    
    value: str
    
    def __post_init__(self):
        """Validate email format."""
        if not self.value:
            raise ValueError("Email cannot be empty")
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    def __str__(self) -> str:
        """Return email as string."""
        return self.value
    
    def to_sha1_hash(self) -> str:
        """Convert email to SHA-1 hash for HIBP API."""
        import hashlib
        return hashlib.sha1(self.value.lower().encode()).hexdigest().upper()
