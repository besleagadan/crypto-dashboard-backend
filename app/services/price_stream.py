import asyncio
import json
from datetime import datetime
from websockets import connect

from app.core.config import settings
from app.services.mongo_service import mongo_service


async def listen_price(symbol: str):
    stream_name = f"{symbol.lower()}@trade"
    url = f"{settings.BINANCE_WS_URL}/{stream_name}"

    async with connect(url) as websocket:
        async for message in websocket:
            data = json.loads(message)
            price_tick = {
                "symbol": symbol.upper(),
                "price": float(data["p"]),
                "timestamp": datetime.fromtimestamp(data["T"] / 1000),
            }
            await mongo_service.insert_price(price_tick)
