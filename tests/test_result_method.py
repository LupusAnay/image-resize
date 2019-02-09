import time

from tests.base_test_case import BaseTestCase


class TestResultMethod(BaseTestCase):
    def setUp(self):
        super().setUp()
        file = {'width': 1000,
                'height': 1000,
                'file': open('images/henculus-avatar.jpg', 'rb')}
        response = self.client.post('/operation/resize',
                                    content_type='multipart/form-data',
                                    data=file)

        self.task_id = response.get_json()['task_id']

    def test_result_method(self):
        time.sleep(.5)
        response = self.client.get(f'/operation/result/{self.task_id}')
        data = response.get_data()
        with open('images/test_response.jpg', 'wb') as file:
            file.write(data)
