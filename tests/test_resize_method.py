from flask import Response

from tests.base_test_case import BaseTestCase


class TestResizeMethod(BaseTestCase):
    def test_resize_image_method(self):
        file = {'width': 100,
                'height': 100,
                'file': open('images/henculus-avatar.jpg', 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(response.status_code, 202)

        data = response.get_json()

        self.assertEqual(data['status'], 'accepted')
        self.assertIsNotNone(data['task_id'])
