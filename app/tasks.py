import os

from PIL import Image
from celery import Celery
from app.config import BaseConfig

celery = Celery(
    __name__,
    backend=BaseConfig.CELERY_RESULT_BACKEND,
    broker=BaseConfig.CELERY_BROKER_URL
)


@celery.task()
def resize_image(filename: str, width: int, height: int) -> None:
    path = os.path.join(BaseConfig.UPLOAD_FOLDER, filename)
    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path)
