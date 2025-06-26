import httpx
from datetime import datetime
from app.celery_worker import celery_app

@celery_app.task
def sync_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = httpx.get(url, params=params)
    coins = response.json()

    print(f"[{datetime.now()}] Top coins synced:")
    for coin in coins:
        print(f"{coin['symbol']} - ${coin['current_price']}")
