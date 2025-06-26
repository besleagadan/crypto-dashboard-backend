from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from typing import List, Dict
# from app.schemas.price import PriceTick
# from app.core.config import settings

from app.db.mongo import mongo_client

class MongoService:
    async def get_prices(self, symbol: str, limit: int = 1):
        db = mongo_client.get_db()
        cursor = db.prices.find({"symbol": symbol.upper()}).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def insert_price(self, price_tick: Dict):
        db = mongo_client.get_db()
        await db.prices.insert_one(price_tick)

mongo_service = MongoService()
