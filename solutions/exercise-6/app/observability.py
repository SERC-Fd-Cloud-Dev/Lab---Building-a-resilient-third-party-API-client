import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger('resilience_lab')
ALLOWED = {'request_id', 'dependency', 'attempt', 'delay', 'kind', 'state',
           'previous_state', 'age_seconds', 'status', 'duration_ms'}

def event(name, *, level=None, **fields):
    if level is None:
        level = logging.WARNING if name in {'retry_scheduled','fallback_used','cache_unavailable'} else (
            logging.ERROR if name == 'request_failed' else logging.INFO)
    record = {'timestamp':datetime.now(timezone.utc).isoformat(),
              'level':logging.getLevelName(level), 'event':name}
    record.update({key:value for key,value in fields.items() if key in ALLOWED})
    logger.log(level, json.dumps(record, separators=(',', ':')))
