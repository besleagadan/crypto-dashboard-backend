from app.services.leaderboard import update_leaderboard
from app.db.postgres import get_db

def handle_trade_event(user_id: int):
    db = next(get_db())
    update_leaderboard(user_id, db)
