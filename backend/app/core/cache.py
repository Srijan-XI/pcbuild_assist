"""
In-memory caching for PCBuild Assist API.
Provides TTL-based caching for expensive operations.
"""
from functools import wraps
from typing import Optional, Any, Callable
import hashlib
import json
import os
from cachetools import TTLCache
from threading import Lock

# Cache configuration
DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", 300))  # 5 minutes default
MAX_CACHE_SIZE = int(os.getenv("CACHE_MAX_SIZE", 1000))

# Thread-safe caches for different data types
_caches = {
    "search": TTLCache(maxsize=MAX_CACHE_SIZE, ttl=DEFAULT_TTL),
    "components": TTLCache(maxsize=MAX_CACHE_SIZE * 2, ttl=DEFAULT_TTL * 2),  # Longer TTL for components
    "facets": TTLCache(maxsize=100, ttl=DEFAULT_TTL * 6),  # 30 min for facets
    "suggestions": TTLCache(maxsize=MAX_CACHE_SIZE, ttl=DEFAULT_TTL),
}
_locks = {key: Lock() for key in _caches}


class CacheManager:
    """Manages multiple cache stores with different TTLs."""
    
    @staticmethod
    def _make_key(*args, **kwargs) -> str:
        """Generate a cache key from function arguments."""
        key_data = {
            "args": args,
            "kwargs": {k: v for k, v in sorted(kwargs.items())}
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    @classmethod
    def get(cls, cache_name: str, key: str) -> Optional[Any]:
        """Get a value from cache."""
        cache = _caches.get(cache_name)
        if cache is None:
            return None
        
        with _locks[cache_name]:
            return cache.get(key)
    
    @classmethod
    def set(cls, cache_name: str, key: str, value: Any) -> None:
        """Set a value in cache."""
        cache = _caches.get(cache_name)
        if cache is None:
            return
        
        with _locks[cache_name]:
            cache[key] = value
    
    @classmethod
    def delete(cls, cache_name: str, key: str) -> None:
        """Delete a value from cache."""
        cache = _caches.get(cache_name)
        if cache is None:
            return
        
        with _locks[cache_name]:
            cache.pop(key, None)
    
    @classmethod
    def clear(cls, cache_name: Optional[str] = None) -> None:
        """Clear a specific cache or all caches."""
        if cache_name:
            cache = _caches.get(cache_name)
            if cache:
                with _locks[cache_name]:
                    cache.clear()
        else:
            for name, cache in _caches.items():
                with _locks[name]:
                    cache.clear()
    
    @classmethod
    def stats(cls) -> dict:
        """Get cache statistics."""
        return {
            name: {
                "size": len(cache),
                "max_size": cache.maxsize,
                "ttl": cache.ttl,
                "hits": getattr(cache, '_hits', 0),
            }
            for name, cache in _caches.items()
        }


# Convenience instance
cache = CacheManager()


def cached(cache_name: str = "search", key_prefix: str = ""):
    """
    Decorator for caching function results.
    
    Args:
        cache_name: Name of the cache store to use
        key_prefix: Optional prefix for cache keys
        
    Example:
        @cached("components", "get_by_id")
        def get_component(component_id: str):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{cache._make_key(*args, **kwargs)}" if key_prefix else cache._make_key(*args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_name, key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            if result is not None:
                cache.set(cache_name, key, result)
            
            return result
        
        # Add cache bypass method
        wrapper.uncached = func
        wrapper.cache_clear = lambda: cache.clear(cache_name)
        
        return wrapper
    return decorator


def cached_async(cache_name: str = "search", key_prefix: str = ""):
    """
    Decorator for caching async function results.
    
    Args:
        cache_name: Name of the cache store to use
        key_prefix: Optional prefix for cache keys
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{cache._make_key(*args, **kwargs)}" if key_prefix else cache._make_key(*args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_name, key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                cache.set(cache_name, key, result)
            
            return result
        
        wrapper.uncached = func
        wrapper.cache_clear = lambda: cache.clear(cache_name)
        
        return wrapper
    return decorator
