import os

basedir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(basedir, '..', 'images')


class BaseConfig:
    DEBUG = False
    ALLOWED_EXTENSIONS = {'jpg', 'png'}


class TestingConfig(BaseConfig):
    TEST_DIR = '../tests/test_images/'
    TEST_IMAGE = os.path.join(TEST_DIR, 'test.jpg')
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
