import os

from flask import Flask
from flask_cors import CORS


def create_app(config_filename='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    CORS(app)

    app_settings = os.getenv(
        'APP_SETTINGS',
        config_filename
    )

    app.config.from_object(app_settings)

    return app
