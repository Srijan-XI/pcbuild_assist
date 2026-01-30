"""
Rate limiting for PCBuild Assist API.
Prevents abuse and ensures fair usage.
"""
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

# Rate limit configuration
DEFAULT_RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")
SEARCH_RATE_LIMIT = os.getenv("SEARCH_RATE_LIMIT", "30/minute")
HEAVY_RATE_LIMIT = os.getenv("HEAVY_RATE_LIMIT", "10/minute")


def get_client_ip(request: Request) -> str:
    """
    Get client IP address, considering proxies.
    """
    # Check for forwarded header (when behind a proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(
    key_func=get_client_ip,
    default_limits=[DEFAULT_RATE_LIMIT],
    storage_uri="memory://",
    strategy="fixed-window"
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.
    """
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": f"Rate limit exceeded: {exc.detail}",
                "retry_after": getattr(exc, 'retry_after', 60)
            }
        },
        headers={
            "Retry-After": str(getattr(exc, 'retry_after', 60)),
            "X-RateLimit-Limit": str(exc.detail) if exc.detail else DEFAULT_RATE_LIMIT
        }
    )


# Rate limit decorators for different endpoint types
def limit_search():
    """Rate limit decorator for search endpoints."""
    return limiter.limit(SEARCH_RATE_LIMIT)


def limit_heavy():
    """Rate limit decorator for computationally heavy endpoints."""
    return limiter.limit(HEAVY_RATE_LIMIT)


def limit_default():
    """Rate limit decorator with default limits."""
    return limiter.limit(DEFAULT_RATE_LIMIT)
