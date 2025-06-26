import asyncio
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.models.leaderboard import Leaderboard
from app.schemas.leaderboard import LeaderboardEntry

router = APIRouter()

@router.get("/", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    # return [{"user_id": 1, "profit": 1}]
    top = db.query(Leaderboard).order_by(Leaderboard.profit.desc()).limit(10).all()
    return top

@router.websocket("/ws/")
async def websocket_leaderboard(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Replace with real pub/sub logic or DB poll
            await websocket.send_json({"event": "leaderboard_update"})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
