from fastapi.testclient import TestClient
from app.main import create_app

def test_baseline_health_and_contract():
    with TestClient(create_app()) as c:
        assert c.get('/health').json()=={'status':'ok'}
        r=c.get('/availability/drill-01')
        assert r.status_code==200
        assert r.json()['product']['available']==7
        assert r.json()['stale'] is False
        assert r.headers['x-request-id']

def test_lab_controls_and_cache_hit():
    with TestClient(create_app()) as c:
        c.get('/availability/drill-01')
        assert c.get('/availability/drill-01').json()['source']=='cache'
        assert c.get('/lab/state').json()['upstream_calls']==1
        assert c.post('/lab/reset').json()=={'reset':True}
        assert c.put('/lab/scenario',json={'scenario':'unavailable'}).status_code==200
        r=c.get('/availability/drill-01')
        assert r.status_code==503
        assert r.headers['content-type'].startswith('application/problem+json')
        assert r.json()['status']==r.status_code

def test_invalid_data_and_not_found():
    with TestClient(create_app()) as c:
        for mode,status in [('invalid',502),('missing',404),('unauthorised',502)]:
            c.post('/lab/reset')
            c.put('/lab/scenario',json={'scenario':mode})
            assert c.get('/availability/drill-01').status_code==status
