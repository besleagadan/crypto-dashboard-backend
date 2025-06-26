from typing import List
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logger import logger
from app.schemas.price import PriceTick
from app.services.mongo_service import mongo_service

router = APIRouter()

@router.get("/{symbol}", response_model=List[PriceTick])
async def get_prices(symbol: str, limit: int = 50):
    return await mongo_service.get_prices(symbol, limit)

@router.websocket("/ws/{symbol}")
async def websocket_prices(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            prices = await mongo_service.get_prices(symbol, limit=1)
            if prices:
                await websocket.send_json({
                    "symbol": prices[0]["symbol"],
                    "price": prices[0]["price"],
                    "timestamp": prices[0]["timestamp"].isoformat()
                })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {symbol}")
