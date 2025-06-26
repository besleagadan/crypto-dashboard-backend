from sqlalchemy.orm import Session
from app.models.trade import Trade
from app.models.leaderboard import Leaderboard

def calculate_user_profit(user_id: int, db: Session) -> float:
    trades = db.query(Trade).filter_by(user_id=user_id).all()
    balance = 0

    for trade in trades:
        sign = 1 if trade.side == "sell" else -1
        balance += sign * trade.price * trade.amount

    return round(balance, 2)

def update_leaderboard(user_id: int, db: Session):
    profit = calculate_user_profit(user_id, db)
    entry = db.query(Leaderboard).filter_by(user_id=user_id).first()
    if entry:
        entry.profit = profit
    else:
        entry = Leaderboard(user_id=user_id, profit=profit)
        db.add(entry)
    db.commit()
