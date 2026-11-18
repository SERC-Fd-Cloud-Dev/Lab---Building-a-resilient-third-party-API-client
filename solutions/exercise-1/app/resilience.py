import asyncio
import httpx
from .errors import UpstreamFailure

def request_timeout():
    # Exercise 2: explicit connect/read/write/pool limits, all 0.5 seconds.
    return httpx.Timeout(5.0)

async def retry_call(operation, *, sleep=asyncio.sleep, emit=lambda *a, **k: None):
    # Working baseline: one attempt. Exercise 2 adds a bounded loop here.
    return await operation()
