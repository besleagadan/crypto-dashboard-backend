from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True
