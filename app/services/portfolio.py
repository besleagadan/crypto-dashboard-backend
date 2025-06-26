from sqlalchemy.orm import Session
from app.models.trade import Trade

def calculate_portfolio(user_id: int, db: Session):
    trades = db.query(Trade).filter(Trade.user_id == user_id).all()
    portfolio = {}

    for trade in trades:
        symbol = trade.symbol
        qty = trade.amount if trade.side == "buy" else -trade.amount
        portfolio[symbol] = portfolio.get(symbol, 0) + qty

    return portfolio
