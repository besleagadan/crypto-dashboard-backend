from datetime import datetime, timedelta
from app.db.mongodb import prices_collection
from app.celery_worker import celery_app

@celery_app.task
async def clean_old_prices():
    cutoff = datetime.utcnow() - timedelta(hours=24)
    result = await prices_collection.delete_many({"timestamp": {"$lt": cutoff}})
    print(f"Deleted {result.deleted_count} old price entries.")
