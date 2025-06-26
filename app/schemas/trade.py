from pydantic import BaseModel
from datetime import datetime

class TradeCreate(BaseModel):
    symbol: str
    price: float
    amount: float
    side: str  # buy/sell

class TradeOut(TradeCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
