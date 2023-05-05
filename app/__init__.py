from flask import Flask, render_template
from config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    return app

app = create_app()


from . import routes
