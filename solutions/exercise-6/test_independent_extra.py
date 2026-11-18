import json
import logging
from fastapi.testclient import TestClient
from app.main import create_app

def test_rate_limit_contract_and_correlation(caplog):
    with caplog.at_level(logging.INFO,logger='resilience_lab'), TestClient(create_app()) as c:
        c.put('/lab/scenario',json={'scenario':'rate-limit'})
        r=c.get('/availability/drill-01')
        assert r.status_code==503
        assert r.headers['content-type'].startswith('application/problem+json')
        assert r.json()['status']==503
        records=[json.loads(x.message) for x in caplog.records if x.name=='resilience_lab']
        own=[x for x in records if x.get('request_id')==r.headers['x-request-id']]
        assert any(x['event']=='request_failed' and x['kind']=='rate_limited' for x in own)
        assert not any(x['event']=='retry_scheduled' for x in own)
        assert c.get('/lab/state').json()['upstream_calls']==1
