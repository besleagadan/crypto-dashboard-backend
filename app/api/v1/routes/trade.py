from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeOut
from app.services.portfolio import calculate_portfolio
from app.db.postgres import get_db

router = APIRouter()

@router.post("/trade", response_model=TradeOut)
def make_trade(data: TradeCreate, user_id: int, db: Session = Depends(get_db)):
    trade = Trade(**data.dict(), user_id=user_id)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

@router.get("/portfolio")
def get_portfolio(user_id: int, db: Session = Depends(get_db)):
    return calculate_portfolio(user_id, db)
