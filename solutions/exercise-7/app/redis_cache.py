import json
from redis.asyncio import Redis
from redis.exceptions import RedisError
from .cache import Entry
from .models import Product
from .cache_policy import RETAIN_SECONDS
from .observability import event

class RedisCache:
    def __init__(self, url, client=None):
        self.client = client if client is not None else Redis.from_url(url,
            decode_responses=True, socket_connect_timeout=0.2, socket_timeout=0.2)

    async def get(self, key):
        try:
            value = await self.client.get('availability:'+key)
            if value is None:
                return None
            data = json.loads(value)
            return Entry(Product.model_validate(data['product']), float(data['saved_at']))
        except (RedisError, ValueError, KeyError, TypeError):
            event('cache_unavailable', dependency='redis')
            return None

    async def set(self, key, entry):
        try:
            await self.client.set('availability:'+key,
                json.dumps({'product':entry.product.model_dump(),'saved_at':entry.saved_at}),
                ex=RETAIN_SECONDS)  # Retain stale-but-usable data beyond freshness.
        except RedisError:
            event('cache_unavailable', dependency='redis')

    async def delete(self, key):
        try:
            await self.client.delete('availability:'+key)
        except RedisError:
            event('cache_unavailable', dependency='redis')

    async def close(self):
        await self.client.aclose()
