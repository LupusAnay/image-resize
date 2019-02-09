import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = False
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'images')
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    ALLOWED_EXTENSIONS = {'jpg', 'png'}


class TestingConfig(BaseConfig):
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
