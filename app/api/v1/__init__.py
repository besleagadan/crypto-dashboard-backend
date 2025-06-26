from fastapi import APIRouter
from .routes import (
    auth,
    prices,
    watchlist,
    trade,
    leaderboard,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(prices.router, prefix="/prices", tags=["Prices"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["Watchlist"])
api_router.include_router(trade.router, prefix="/trade", tags=["Trade"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])
