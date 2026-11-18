from pydantic import BaseModel, Field

class Product(BaseModel):
    sku: str
    name: str
    available: int = Field(ge=0)

class Availability(BaseModel):
    product: Product
    source: str
    stale: bool
    age_seconds: float
