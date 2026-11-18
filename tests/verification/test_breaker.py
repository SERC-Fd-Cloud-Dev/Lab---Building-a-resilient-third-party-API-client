import pytest
import circuitbreaker
from app.errors import UpstreamFailure
from tests.helpers import setup_service, Clock

async def test_open_short_circuit_and_recovery(monkeypatch):
    clock=Clock()
    monkeypatch.setattr(circuitbreaker,'monotonic',clock)
    async with setup_service('unavailable',clock) as (s,sim,delays):
        assert s.breaker is not None
        for count in [1,2]:
            with pytest.raises(UpstreamFailure): await s.get('drill-01','trace')
            assert s.breaker.failure_count==count
        assert sim.calls==6  # Two logical calls, three attempts each.
        assert s.breaker.state=='open'
        with pytest.raises(UpstreamFailure) as e: await s.get('drill-01','trace')
        assert e.value.kind=='circuit_open'
        assert sim.calls==6
        clock.advance(5)
        assert s.breaker.state=='half_open'
        sim.configure('success')
        await s.get('drill-01','trace')
        assert s.breaker.state=='closed'
        assert s.breaker.failure_count==0

async def test_failed_probe_reopens(monkeypatch):
    clock=Clock(); monkeypatch.setattr(circuitbreaker,'monotonic',clock)
    async with setup_service('unavailable',clock) as (s,sim,_):
        assert s.breaker is not None
        for _ in range(2):
            with pytest.raises(UpstreamFailure): await s.get('drill-01','trace')
        clock.advance(5)
        with pytest.raises(UpstreamFailure): await s.get('drill-01','trace')
        assert s.breaker.state=='open'
        assert sim.calls==9

async def test_ignored_error_resets_package_consecutive_count():
    async with setup_service('unavailable') as (s,sim,_):
        assert s.breaker is not None
        with pytest.raises(UpstreamFailure): await s.get('drill-01','trace')
        assert s.breaker.failure_count==1
        sim.configure('unauthorised')
        with pytest.raises(UpstreamFailure): await s.get('drill-01','trace')
        assert s.breaker.failure_count==0  # Package semantics: non-counted errors reset.
