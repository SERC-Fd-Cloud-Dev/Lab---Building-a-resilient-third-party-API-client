import asyncio
import httpx
from .errors import UpstreamFailure

def request_timeout():
    return httpx.Timeout(connect=0.5, read=0.5, write=0.5, pool=0.5)

async def retry_call(operation, *, sleep=asyncio.sleep, emit=lambda *a, **k: None):
    for attempt in range(1, 4):  # Three attempts TOTAL, including the original.
        emit('upstream_attempt', attempt=attempt)
        try:
            return await operation()
        except UpstreamFailure as error:
            if not error.retryable or attempt == 3:
                raise
            delay = 0.1 * 2 ** (attempt - 1)
            emit('retry_scheduled', attempt=attempt, delay=delay, kind=error.kind)
            await sleep(delay)
