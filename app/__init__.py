import os

from flask import Flask
from flask_cors import CORS


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

    flask.logger.info('Views blueprint successfully registered')

    return flask
