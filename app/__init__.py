import os

from celery import Celery
from flask import Flask, current_app
from flask_cors import CORS


def create_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    current_app.logger.info(
        f'Created Celery instance with {app.config["CELERY_RESULT_BACKEND"]}'
        f'as backend and with {app.config["CELERY_BROKER_URL"]} as broker')

    return celery


def create_app(config_filename: str = 'app.config.DevelopmentConfig') -> Flask:
    app = Flask(__name__)
    CORS(app)

    app_settings = os.getenv(
        'APP_SETTINGS',
        config_filename
    )

    app.config.from_object(app_settings)

    app.logger.info(
        f'Created Flask instance with {config_filename} as config'
    )

    from app import views
    app.register_blueprint(views.blueprint)

    app.logger.info('Views blueprint successfully registered')

    return app
