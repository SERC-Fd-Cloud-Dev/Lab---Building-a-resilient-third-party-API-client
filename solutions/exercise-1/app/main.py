import logging
import os
import time
from uuid import uuid4
from contextlib import asynccontextmanager
from typing import Literal
import httpx
from fastapi import FastAPI, Request
from pydantic import BaseModel
from .supplier import SupplierSimulator
from .service import SupplierService
from .resilience import request_timeout
from .models import Availability
from .errors import UpstreamFailure, problem
from .observability import event

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

class Scenario(BaseModel):
    scenario: Literal['success','flaky','timeout','connection','unavailable',
                      'invalid','missing','unauthorised','rate-limit']

def create_app(*, transport=None, clock=time.time, sleep=None):
    simulator = SupplierSimulator()

    @asynccontextmanager
    async def lifespan(api):
        cache = None
        if os.getenv('CACHE_BACKEND') == 'redis':
            from .redis_cache import RedisCache
            cache = RedisCache(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
        async with httpx.AsyncClient(base_url='https://supplier.test',
                transport=transport or httpx.MockTransport(simulator.handle),
                timeout=request_timeout()) as client:
            options = {'cache':cache, 'clock':clock}
            if sleep is not None:
                options['sleep'] = sleep
            api.state.service = SupplierService(client, **options)
            yield
            await api.state.service.cache.close()

    api = FastAPI(title='Workshop Supplies API', version='1.0', lifespan=lifespan)

    @api.middleware('http')
    async def correlation(request: Request, call_next):
        # Generate trusted IDs locally. Do not echo unvalidated input into logs.
        request.state.request_id = str(uuid4())
        started = time.monotonic()
        response = await call_next(request)
        response.headers['X-Request-ID'] = request.state.request_id
        event('request_complete', request_id=request.state.request_id,
              status=response.status_code, duration_ms=round((time.monotonic()-started)*1000, 2))
        return response

    @api.get('/health')
    async def health():
        return {'status':'ok'}

    @api.get('/availability/{sku}', response_model=Availability)
    async def availability(sku: str, request: Request):
        try:
            return await api.state.service.get(sku, request.state.request_id)
        except UpstreamFailure as error:
            return problem(error, request.state.request_id)

    # Lab-only controls. Never include these endpoints in a deployed application.
    @api.put('/lab/scenario')
    async def scenario(body: Scenario):
        simulator.configure(body.scenario)
        return {'scenario':simulator.scenario, 'calls':simulator.calls}

    @api.get('/lab/state')
    async def state():
        breaker = api.state.service.breaker
        return {'scenario':simulator.scenario, 'upstream_calls':simulator.calls,
                'breaker':breaker.state if breaker else 'disabled',
                'failure_count':breaker.failure_count if breaker else 0}

    @api.post('/lab/reset')
    async def reset():
        simulator.configure('success')
        await api.state.service.cache.delete('drill-01')
        if api.state.service.breaker:
            api.state.service.breaker.reset()
        api.state.service.last_state = 'closed'
        return {'reset':True}
    return api

app = create_app()
