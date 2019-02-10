from PIL import Image
from flask import current_app

from app.tasks import resize_image
from tests.base_test_case import BaseTestCase


class TestResizeTask(BaseTestCase):
    def test_resize(self, *_):
        w = 300
        h = 500
        with open(current_app.config['TEST_IMAGE'], 'rb') as file:
            resize_image(file.name, w, h)

            img = Image.open(file)
            self.assertEqual((w, h), img.size)
