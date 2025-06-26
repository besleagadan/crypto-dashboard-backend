from pydantic import BaseModel

class WatchlistCreate(BaseModel):
    symbol: str

class WatchlistOut(WatchlistCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
