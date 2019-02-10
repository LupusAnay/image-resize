import time
import uuid

from tests.base_test_case import BaseTestCase


class TestResultMethod(BaseTestCase):
    def setUp(self):
        super().setUp()
        file = {'width': 1000,
                'height': 1000,
                'file': open('test_images/test.jpg', 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)
        self.assertEqual(202, response.status_code)

        self.task_id = response.get_json()['task_id']

    def test_result_method(self):
        time.sleep(.5)
        response = self.client.get(f'/operation/result/{self.task_id}')
        self.assert200(response)
        data = response.get_data()
        with open('test_images/response.jpg', 'wb') as file:
            file.write(data)

    def test_status_with_invalid_id(self):
        invalid_id = uuid.uuid4()
        response = self.client.get(f'/status/{str(invalid_id)}')
        self.assert404(response)
        data = response.get_json()
        self.assertEqual('error', data['result'])
