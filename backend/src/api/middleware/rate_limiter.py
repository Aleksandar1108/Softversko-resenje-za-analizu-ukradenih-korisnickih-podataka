"""Rate limiting middleware."""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

from fastapi import Request, HTTPException, status


class RateLimiter:
    """Simple rate limiter (in production, use Redis)."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if request is allowed.
        
        Args:
            client_id: Client identifier (IP address)
            
        Returns:
            True if request is allowed
        """
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_client_id(self, request: Request) -> str:
        """Get client identifier from request."""
        return request.client.host if request.client else "unknown"


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    # Skip rate limiting for OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return await call_next(request)
    
    client_id = rate_limiter.get_client_id(request)
    
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
    
    response = await call_next(request)
    return response
