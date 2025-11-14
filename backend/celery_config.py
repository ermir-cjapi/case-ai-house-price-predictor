"""
Celery application configuration
Sets up Celery with Redis broker for asynchronous task processing
"""
from celery import Celery
from config import REDIS_URL, CELERY_CONFIG

# Create Celery app
celery_app = Celery(
    'house_price_predictor',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['celery_worker']  # Import tasks module
)

# Celery configuration
celery_app.conf.update(**CELERY_CONFIG)

if __name__ == '__main__':
    celery_app.start()

