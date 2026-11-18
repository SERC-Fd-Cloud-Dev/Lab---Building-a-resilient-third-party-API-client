"""Deterministic transport. Exceptions are injected; it does not prove socket timing."""
import httpx

PRODUCT = {'sku': 'drill-01', 'name': 'Cordless drill', 'available': 7}

class SupplierSimulator:
    def __init__(self):
        self.configure('success')

    def configure(self, scenario):
        self.scenario, self.calls = scenario, 0

    async def handle(self, request):
        self.calls += 1
        mode = self.scenario
        if mode == 'flaky' and self.calls == 1:
            return httpx.Response(503)
        if mode == 'timeout':
            raise httpx.ReadTimeout('simulated', request=request)
        if mode == 'connection':
            raise httpx.ConnectError('simulated', request=request)
        if mode == 'invalid':
            return httpx.Response(200, json={'available': 'unknown'})
        if mode in {'unavailable', 'missing', 'unauthorised', 'rate-limit'}:
            return httpx.Response({'unavailable':503, 'missing':404,
                'unauthorised':401, 'rate-limit':429}[mode], headers={'Retry-After':'20'})
        return httpx.Response(200, json=PRODUCT)
