import time
import uuid

from tests.base_test_case import BaseTestCase


class TestStatusMethod(BaseTestCase):
    def setUp(self):
        super().setUp()
        file = {'width': 100,
                'height': 100,
                'file': open('images/henculus-avatar.jpg', 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)

        self.task_id = response.get_json()['task_id']

    def test_status_method(self):
        states = {'PENDING', 'SENT', 'STARTED', 'RETRY', 'FAILURE', 'SUCCESS'}

        response_1 = self.client.get(f'/status/{self.task_id}')
        self.assert200(response_1)
        data = response_1.get_json()
        self.assertIn(data['status'], states)
        self.logger.info(data['status'])

        time.sleep(0.1)

        response_2 = self.client.get(f'/status/{self.task_id}')
        self.assert200(response_2)
        data = response_2.get_json()
        self.assertIn(data['status'], states)
        self.logger.info(data['status'])

    def test_status_with_invalid_id(self):
        invalid_id = uuid.uuid4()
        response = self.client.get(f'/status/{str(invalid_id)}')
        self.logger.info(response.status_code)
        data = response.get_json()
        self.logger.info(data)
