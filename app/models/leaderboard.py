from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import AbstractBaseModel

class Leaderboard(AbstractBaseModel):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    profit = Column(Float, default=0.0)

    user = relationship("User", foreign_keys=[user_id])
