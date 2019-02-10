import os
from typing import Union

from PIL import Image
from celery import Celery

from app.config import upload_dir

os.environ['CELERY_CONFIG_MODULE'] = 'app.celeryconfig'

celery = Celery(
    'tasks'
)


@celery.task()
def resize_image(filename: str, width: int, height: int) -> Union[bytes, str]:
    """
    Async celery task, resizing image in upload dir with given filename

    :param filename: Name of image in upload dir to resize
    :param width: Target width
    :param height: Target height
    :return: Path to processed file
    """
    path = os.path.join(upload_dir, filename)

    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path)

    return str(path)
