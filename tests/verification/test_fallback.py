import pytest
from app.errors import UpstreamFailure
from tests.helpers import setup_service, Clock

async def test_fresh_stale_and_retention_boundary():
    clock=Clock()
    async with setup_service(clock=clock) as (s,sim,_):
        await s.get('drill-01','seed')
        clock.advance(9)
        assert (await s.get('drill-01','fresh')).source=='cache'
        assert sim.calls==1
        clock.advance(1)
        sim.configure('unavailable')
        result=await s.get('drill-01','stale')
        assert (result.source,result.stale,result.age_seconds)==('fallback',True,10.0)
        assert s.breaker.failure_count==1  # Fallback did not hide failure.
        result=await s.get('drill-01','again')
        assert s.breaker.state=='open'
        calls=sim.calls
        assert (await s.get('drill-01','open')).source=='fallback'
        assert sim.calls==calls
        clock.advance(50)
        with pytest.raises(UpstreamFailure): await s.get('drill-01','expired')

async def test_permanent_failure_does_not_use_stale_data():
    clock=Clock()
    async with setup_service(clock=clock) as (s,sim,_):
        await s.get('drill-01','seed')
        clock.advance(11)
        sim.configure('missing')
        with pytest.raises(UpstreamFailure) as e: await s.get('drill-01','trace')
        assert e.value.status==404
        assert sim.calls==1

async def test_cache_is_keyed():
    async with setup_service() as (s,sim,_):
        await s.get('drill-01','seed')
        sim.configure('unavailable')
        with pytest.raises(UpstreamFailure): await s.get('saw-02','other')
