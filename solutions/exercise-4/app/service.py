import asyncio
import time
import httpx
from pydantic import ValidationError
from circuitbreaker import CircuitBreakerError
from .models import Product, Availability
from .errors import UpstreamFailure, classify_status
from .resilience import retry_call
from .breaker import make_breaker
from .cache import Entry, MemoryCache
from .cache_policy import FRESH_SECONDS, RETAIN_SECONDS, may_fallback
from .observability import event

class SupplierService:
    def __init__(self, client, *, cache=None, clock=time.time, sleep=asyncio.sleep):
        self.client, self.clock, self.sleep = client, clock, sleep
        self.cache = cache if cache is not None else MemoryCache()
        self.breaker = make_breaker()
        # Breaker wraps the entire retry operation. Fallback sits OUTSIDE it.
        self.protected = self.breaker(self._with_retries) if self.breaker else self._with_retries
        self.last_state = 'closed'

    def emit(self, name, request_id, **fields):
        event(name, request_id=request_id, dependency='supplier', **fields)

    async def _once(self, sku):
        try:
            response = await self.client.get(f'/products/{sku}')
        except httpx.TimeoutException:
            raise UpstreamFailure('timeout', 504, True, True) from None
        except httpx.TransportError:
            raise UpstreamFailure('connection', 503, True, True) from None
        if response.status_code != 200:
            raise classify_status(response.status_code)
        try:
            product = Product.model_validate(response.json())
            if product.sku != sku:
                raise ValueError('sku mismatch')
            return product
        except (ValueError, ValidationError):
            raise UpstreamFailure('invalid_response', 502) from None

    async def _with_retries(self, sku, request_id):
        try:
            async with asyncio.timeout(2.0):
                return await retry_call(lambda: self._once(sku), sleep=self.sleep,
                    emit=lambda name, **fields: self.emit(name, request_id, **fields))
        except TimeoutError:
            raise UpstreamFailure('timeout', 504, True, True) from None

    def report_state(self, request_id):
        state = self.breaker.state if self.breaker else 'disabled'
        if state != self.last_state:
            self.emit('circuit_state', request_id, previous_state=self.last_state, state=state)
            self.last_state = state

    def response(self, entry, source):
        age = max(0, self.clock() - entry.saved_at)
        return Availability(product=entry.product, source=source,
                            stale=age >= FRESH_SECONDS, age_seconds=round(age, 3))

    async def get(self, sku, request_id):
        entry = await self.cache.get(sku)
        now = self.clock()
        # Freshness and retention are distinct. Remove entries too old for fallback.
        if entry and not 0 <= now - entry.saved_at < RETAIN_SECONDS:
            await self.cache.delete(sku)
            entry = None
        if entry and now - entry.saved_at < FRESH_SECONDS:
            self.emit('cache_hit', request_id, age_seconds=now-entry.saved_at)
            return self.response(entry, 'cache')
        self.report_state(request_id)
        try:
            product = await self.protected(sku, request_id)
        except CircuitBreakerError:
            error = UpstreamFailure('circuit_open', 503, False, True)
        except UpstreamFailure as exc:
            error = exc
        else:
            entry = Entry(product, self.clock())
            await self.cache.set(sku, entry)
            self.report_state(request_id)
            self.emit('upstream_success', request_id)
            return self.response(entry, 'upstream')
        self.report_state(request_id)
        if may_fallback(entry, self.clock(), error):
            self.emit('fallback_used', request_id, kind=error.kind,
                      age_seconds=self.clock()-entry.saved_at)
            return self.response(entry, 'fallback')
        self.emit('request_failed', request_id, kind=error.kind, status=error.status)
        raise error
