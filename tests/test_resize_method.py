from tests.base_test_case import BaseTestCase


class TestResizeMethod(BaseTestCase):
    def test_resize_image(self):
        file = {'width': 100,
                'height': 100,
                'file': open('images/henculus-avatar.jpg', 'rb')}
        self.client.post('/operation/resize',
                         content_type='multipart/form-data',
                         data=file)
