from flask import current_app

from tests.base_test_case import BaseTestCase


class TestResizeMethod(BaseTestCase):
    def test_resize_image_method(self):
        file = {'width': 100,
                'height': 100,
                'file': open(current_app.config['TEST_IMAGE'], 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(202, response.status_code)

        data = response.get_json()

        self.assertEqual(data['status'], 'accepted')
        self.assertIsNotNone(data['task_id'])

    def test_resize_image_method_with_invalid_size(self):
        file = {'width': 0,
                'height': 0,
                'file': open(current_app.config['TEST_IMAGE'], 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(422, response.status_code)

    def test_resize_image_method_with_invalid_file(self):
        file = {'width': 10,
                'height': 10,
                'file': ''}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(422, response.status_code)
