"""
backend/middleware/cache.py
Simple in-memory cache for expensive DB queries.
"""
import time
from functools import wraps

_cache = {}

def cache_get(key):
    item = _cache.get(key)
    if item and time.time() < item['expires']:
        return item['value']
    return None

def cache_set(key, value, ttl=300):
    _cache[key] = {'value': value, 'expires': time.time() + ttl}

def cache_clear(prefix=None):
    global _cache
    if prefix:
        _cache = {k: v for k, v in _cache.items() if not k.startswith(prefix)}
    else:
        _cache = {}

def cached(ttl=300):
    """Decorator — caches function result by args for ttl seconds."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = f"{fn.__name__}:{args}:{sorted(kwargs.items())}"
            result = cache_get(key)
            if result is not None:
                return result
            result = fn(*args, **kwargs)
            cache_set(key, result, ttl)
            return result
        return wrapper
    return decorator

def cache_stats():
    now = time.time()
    active = {k: v for k, v in _cache.items() if now < v['expires']}
    return {'total_keys': len(_cache), 'active_keys': len(active)}
