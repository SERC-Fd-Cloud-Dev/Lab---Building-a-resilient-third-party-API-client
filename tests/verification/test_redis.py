import fakeredis.aioredis
from redis.exceptions import ConnectionError
from app.redis_cache import RedisCache
from app.cache import Entry
from app.models import Product

async def test_retention_ttl_and_round_trip():
    client=fakeredis.aioredis.FakeRedis(decode_responses=True)
    cache=RedisCache('',client=client)
    item=Entry(Product(sku='drill-01',name='Drill',available=7),100.0)
    await cache.set('drill-01',item)
    assert (await cache.get('drill-01')).product.available==7
    assert 59<=await client.ttl('availability:drill-01')<=60
    await cache.delete('drill-01')
    assert await cache.get('drill-01') is None
    await cache.close()

async def test_redis_outage_behaves_as_cache_miss():
    class Broken:
        async def get(self,key): raise ConnectionError('secret details')
        async def set(self,*a,**kw): raise ConnectionError('secret details')
        async def delete(self,key): raise ConnectionError('secret details')
    cache=RedisCache('',client=Broken())
    assert await cache.get('drill-01') is None
    await cache.set('drill-01',Entry(Product(sku='drill-01',name='Drill',available=7),100))
    await cache.delete('drill-01')
