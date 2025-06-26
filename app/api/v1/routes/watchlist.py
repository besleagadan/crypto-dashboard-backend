from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate, WatchlistOut
from app.db.postgres import get_db

router = APIRouter()

@router.get("/", response_model=list[WatchlistOut])
def get_watchlist(user_id: int, db: Session = Depends(get_db)):
    print("_____ START")
    return [{"id": 1, "user_id": 1}]
    return db.query(Watchlist).filter_by(user_id=user_id).all()

# @router.get("/")
# def get_watchlist(user_id: int):
#     print("_____ START")
#     return {}
#     return db.query(Watchlist).filter_by(user_id=user_id).all()

@router.post("", response_model=WatchlistOut)
def add_to_watchlist(data: WatchlistCreate, user_id: int, db: Session = Depends(get_db)):
    entry = Watchlist(**data.dict(), user_id=user_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
