from pydantic import BaseModel

class LeaderboardEntry(BaseModel):
    user_id: int
    profit: float

    class Config:
        orm_mode = True
