import os
from typing import Union

from logging import getLogger
from PIL import Image
from celery import Celery

from app.config import BaseConfig, upload_dir

celery = Celery(
    __name__,
    backend=BaseConfig.CELERY_RESULT_BACKEND,
    broker=BaseConfig.CELERY_BROKER_URL
)

logger = getLogger()


@celery.task()
def resize_image(filename: str, width: int, height: int) -> Union[bytes, str]:
    path = os.path.join(upload_dir, filename)
    logger.debug(path)

    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path)

    return str(path)
