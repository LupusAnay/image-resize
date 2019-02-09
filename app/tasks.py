import os
from typing import Union

from PIL import Image
from celery import Celery

from app.config import upload_dir, BaseConfig

celery = Celery(
    'tasks',
    backend=BaseConfig.CELERY_RESULT_BACKEND,
    broker=BaseConfig.CELERY_BROKER_URL
)


@celery.task()
def resize_image(filename: str, width: int, height: int) -> Union[bytes, str]:
    path = os.path.join(upload_dir, filename)

    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path)

    return str(path)
