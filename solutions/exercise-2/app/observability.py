import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger('resilience_lab')
ALLOWED = {'request_id', 'dependency', 'attempt', 'delay', 'kind', 'state',
           'previous_state', 'age_seconds', 'status', 'duration_ms'}

def event(name, *, level=logging.INFO, **fields):
    # Exercise 5: JSON record using only ALLOWED fields; exclude arbitrary payloads.
    pass
