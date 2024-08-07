import os

from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery(__name__, broker=redis_url, backend=redis_url)
app.conf["imports"] = ("src.api.tasks",)
