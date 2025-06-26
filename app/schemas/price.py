from pydantic import BaseModel
from datetime import datetime

class PriceTick(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
