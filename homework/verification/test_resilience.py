import json
import logging
import httpx
import pytest
from movie_game.services.tmdb import TMDBService,TMDBFailure
from movie_game.main import create_app
from movie_game.config import Settings
from fastapi.testclient import TestClient

async def test_transient_success_and_logs(caplog):
    calls=[]; delays=[]
    def response(request):
        calls.append(request)
        return httpx.Response(503) if len(calls)==1 else httpx.Response(200,
            json={'id':11,'title':'Example','release_date':'2001-01-01','runtime':112})
    async def sleep(delay): delays.append(delay)
    with caplog.at_level(logging.INFO,logger='movie_game'):
        async with httpx.AsyncClient(base_url='https://api.themoviedb.org',
                headers={'Authorization':'Bearer do-not-log'},transport=httpx.MockTransport(response)) as c:
            assert (await TMDBService(c,sleep=sleep).movie(11,'hw-1')).title=='Example'
    assert len(calls)==2
    assert delays==[0.1]
    records=[json.loads(r.message) for r in caplog.records if r.name=='movie_game']
    assert records and all(r['request_id']=='hw-1' for r in records)
    assert 'do-not-log' not in caplog.text

@pytest.mark.parametrize('code,attempts,status',[(503,3,503),(401,1,502),(404,1,404),(429,1,503)])
async def test_failure_bounds(code,attempts,status):
    calls=[]; delays=[]
    def response(request):
        calls.append(request); return httpx.Response(code)
    async def sleep(delay): delays.append(delay)
    async with httpx.AsyncClient(base_url='https://api.themoviedb.org',transport=httpx.MockTransport(response)) as c:
        with pytest.raises(TMDBFailure) as e: await TMDBService(c,sleep=sleep).movie(11,'hw-2')
    assert e.value.status==status
    assert len(calls)==attempts
    assert delays==([0.1,0.2] if attempts==3 else [])

def test_live_credential_is_outgoing_only():
    seen=[]
    def response(request):
        seen.append(request)
        return httpx.Response(503)
    async def sleep(_): pass
    with TestClient(create_app(Settings('outgoing-only','incoming-only',False),httpx.MockTransport(response),sleep)) as c:
        r=c.get('/games/11/answer',headers={'X-API-Key':'incoming-only'})
        assert r.status_code==503
        assert r.json()['status']==503
        assert r.headers['content-type'].startswith('application/problem+json')
    assert all(r.headers['Authorization']=='Bearer outgoing-only' for r in seen)
    assert all('incoming-only' not in str(r.headers) for r in seen)
