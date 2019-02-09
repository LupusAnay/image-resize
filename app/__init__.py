import os
from logging.config import dictConfig

from flask import Flask
from flask_cors import CORS

from app.config import BaseConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(config_filename: str = 'app.config.DevelopmentConfig') -> Flask:
    flask = Flask(__name__)

    CORS(flask)

    app_settings = os.getenv(
        'APP_SETTINGS',
        config_filename
    )

    flask.config.from_object(app_settings)

    flask.logger.info(
        f'Created Flask instance with {config_filename} as config'
    )

    from app import views
    flask.register_blueprint(views.operation_blueprint)
    flask.register_blueprint(views.status_blueprint)

    flask.logger.info('Views blueprints successfully registered')
    # flask.logger.info(f'Celery backend: {celery.backend}')
    # flask.logger.info(f'Celery broker: {celery.broker_connection}')

    return flask
