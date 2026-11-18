import pytest
from app.errors import UpstreamFailure
from app.resilience import request_timeout
from tests.helpers import setup_service

def test_explicit_phase_limits():
    t=request_timeout()
    assert (t.connect,t.read,t.write,t.pool)==(0.5,0.5,0.5,0.5)

async def test_transient_recovery():
    async with setup_service('flaky') as (s,sim,delays):
        assert (await s.get('drill-01','trace-a')).source=='upstream'
        assert sim.calls==2
        assert delays==[0.1]

@pytest.mark.parametrize('mode,status',[('timeout',504),('connection',503),('unavailable',503)])
async def test_exhaustion(mode,status):
    async with setup_service(mode) as (s,sim,delays):
        with pytest.raises(UpstreamFailure) as e:
            await s.get('drill-01','trace-b')
        assert e.value.status==status
        assert sim.calls==3
        assert delays==[0.1,0.2]  # No sleep after the final attempt.

@pytest.mark.parametrize('mode',['missing','unauthorised','invalid'])
async def test_permanent_failures_single_attempt(mode):
    async with setup_service(mode) as (s,sim,delays):
        with pytest.raises(UpstreamFailure): await s.get('drill-01','trace-c')
        assert sim.calls==1
        assert delays==[]
