import os
from logging import getLogger
from flask_testing import TestCase

from app import create_app, config


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('app.config.TestingConfig')

    def setUp(self):
        self.logger = getLogger(__name__)
        self.logger.info('Test execution started')

    def tearDown(self):
        self.logger.info('Clearing upload dir')
        for filename in os.listdir(config.upload_dir):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                os.unlink(os.path.join(config.upload_dir, filename))

        self.logger.info('Test execution finished')
        print('\n')
