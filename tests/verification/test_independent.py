"""Minimum acceptance check. Add your own API, count and log evidence tests."""
import pytest
from app.errors import UpstreamFailure
from tests.helpers import setup_service

async def test_rate_limit_has_controlled_service_response():
    async with setup_service('rate-limit') as (s,sim,delays):
        with pytest.raises(UpstreamFailure) as e: await s.get('drill-01','independent')
        assert e.value.status==503
        assert sim.calls==1
        assert delays==[]
        assert s.breaker.failure_count==0
