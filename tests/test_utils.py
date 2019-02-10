from app import utils
from tests.base_test_case import BaseTestCase


class TestStatusMethod(BaseTestCase):
    def test_size_valid(self):
        data = {'width': 1, 'height': 1}
        self.assertTrue(utils.size_valid(data))
        data = {'width': 0, 'height': 0}
        self.assertFalse(utils.size_valid(data))
        data = {'width': 10000, 'height': 10000}
        self.assertFalse(utils.size_valid(data))
        data = {}
        self.assertFalse(utils.size_valid(data))

    def test_create_response(self):
        response = utils.create_response(1000, test='hello')
        self.assertEqual(1000, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(response.get_json()['test'], 'hello')

    def test_create_error_response(self):
        response = utils.create_error_response(404, 'Test error')
        self.assertEqual(404, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertIn('result', response.get_json())
        self.assertIn('message', response.get_json())
        self.assertEqual(response.get_json()['result'], 'error')
        self.assertEqual(response.get_json()['message'], 'Test error')

    def test_allowed_extension(self):
        self.assertTrue(utils.allowed_extension('image.jpg'))
        self.assertTrue(utils.allowed_extension('image.png'))
        self.assertFalse(utils.allowed_extension('image.ext'))
        self.assertFalse(utils.allowed_extension('image.'))
