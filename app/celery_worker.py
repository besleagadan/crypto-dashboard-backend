from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"}
}
