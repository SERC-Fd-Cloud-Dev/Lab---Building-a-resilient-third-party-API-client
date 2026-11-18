from contextlib import asynccontextmanager
import httpx
from app.service import SupplierService
from app.supplier import SupplierSimulator

class Clock:
    def __init__(self): self.now=100.0
    def __call__(self): return self.now
    def advance(self, seconds): self.now+=seconds

@asynccontextmanager
async def setup_service(mode='success', clock=None):
    simulator=SupplierSimulator()
    simulator.configure(mode)
    delays=[]
    async def sleep(delay): delays.append(delay)
    async with httpx.AsyncClient(base_url='https://supplier.test',
            transport=httpx.MockTransport(simulator.handle)) as client:
        yield SupplierService(client,clock=clock or Clock(),sleep=sleep), simulator, delays
