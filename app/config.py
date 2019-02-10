import os

basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, '..', 'images')


class BaseConfig:
    DEBUG = False
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    ALLOWED_EXTENSIONS = {'jpg', 'png'}


class TestingConfig(BaseConfig):
    TEST_DIR = '../tests/test_images/'
    TEST_IMAGE = os.path.join(TEST_DIR, 'test.jpg')
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
