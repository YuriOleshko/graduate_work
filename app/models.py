from . import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///info.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    token = db.Column(db.String(350))


with app.app_context():
    db.create_all()