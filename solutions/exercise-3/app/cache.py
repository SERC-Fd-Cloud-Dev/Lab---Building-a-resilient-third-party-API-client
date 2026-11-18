from dataclasses import dataclass
from .models import Product

@dataclass
class Entry:
    product: Product
    saved_at: float

class MemoryCache:
    def __init__(self):
        self.entries = {}

    async def get(self, key):
        return self.entries.get(key)

    async def set(self, key, entry):
        self.entries[key] = entry

    async def delete(self, key):
        self.entries.pop(key, None)

    async def close(self):
        pass
