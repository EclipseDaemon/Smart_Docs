import json
import redis.asyncio as aioredis
from typing import Optional, Any
from app.config import settings

_redis_client: Optional[aioredis.Redis] = None


async def get_redis_client() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_client


async def close_redis_client():
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None


async def get_cached(key: str) -> Optional[Any]:
    try:
        client = await get_redis_client()
        value = await client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception:
        return None


async def set_cached(key: str, value: Any, ttl_seconds: int = 300) -> None:
    try:
        client = await get_redis_client()
        await client.setex(
            key,
            ttl_seconds,
            json.dumps(value, default=str)
        )
    except Exception:
        pass


async def delete_cached(key: str) -> None:
    try:
        client = await get_redis_client()
        await client.delete(key)
    except Exception:
        pass


async def delete_pattern(pattern: str) -> None:
    try:
        client = await get_redis_client()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
    except Exception:
        pass


def make_documents_cache_key(user_id: int) -> str:
    return f"user:{user_id}:documents"


def make_search_cache_key(user_id: int, query: str) -> str:
    return f"user:{user_id}:search:{query.lower().strip()}"