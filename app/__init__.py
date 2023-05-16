from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///info.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


with app.app_context():
    db.create_all()

from . import routes
