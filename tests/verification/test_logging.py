import json
import logging
from app.observability import event
from tests.helpers import setup_service

def test_safe_allowlist_and_json(caplog):
    with caplog.at_level(logging.INFO,logger='resilience_lab'):
        event('check',request_id='r1',authorization='secret',url='?api_key=secret',payload='secret')
    records=[json.loads(r.message) for r in caplog.records if r.name=='resilience_lab']
    assert records, 'Implement event() so a JSON record is emitted.'
    assert records[0]['request_id']=='r1'
    assert 'timestamp' in records[0]
    assert 'secret' not in str(records)

async def test_correlated_retry_sequence(caplog):
    with caplog.at_level(logging.INFO,logger='resilience_lab'):
        async with setup_service('flaky') as (s,_,__): await s.get('drill-01','trace-27')
    records=[json.loads(r.message) for r in caplog.records if r.name=='resilience_lab']
    assert [r['event'] for r in records if r['event']!='circuit_state']==[
        'upstream_attempt','retry_scheduled','upstream_attempt','upstream_success']
    assert all(r['request_id']=='trace-27' for r in records)
    assert records[1]['level']=='WARNING'
