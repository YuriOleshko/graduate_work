from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CLIENT_ID = Config.CLIENT_ID
    CLIENT_SECRET = Config.CLIENT_SECRET
    AUTHORIZATION_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
    REDIRECT_URI = 'http://localhost:5000/home'

    return app

app = create_app()

from . import models

from . import routes
