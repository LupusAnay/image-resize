import time
import uuid

from flask import current_app

from tests.base_test_case import BaseTestCase


class TestStatusMethod(BaseTestCase):
    def setUp(self):
        super().setUp()
        file = {'width': 100,
                'height': 100,
                'file': open(current_app.config['TEST_IMAGE'], 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(202, response.status_code)

        self.task_id = response.get_json()['task_id']

    def test_status_method(self):
        states = {'PENDING', 'SENT', 'STARTED', 'RETRY', 'FAILURE', 'SUCCESS'}

        response_1 = self.client.get(f'/status/{self.task_id}')
        self.assert200(response_1)
        data = response_1.get_json()
        self.assertIn(data['status'], states)

        time.sleep(0.1)

        response_2 = self.client.get(f'/status/{self.task_id}')
        self.assert200(response_2)
        data = response_2.get_json()
        self.assertIn(data['status'], states)

    def test_status_with_invalid_id(self):
        invalid_id = uuid.uuid4()
        response = self.client.get(f'/status/{str(invalid_id)}')
        self.assert404(response)
        data = response.get_json()
        self.assertEqual('error', data['result'])
