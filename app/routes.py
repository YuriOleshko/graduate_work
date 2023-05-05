from . import app
from flask import render_template, redirect, url_for
from config import Config

CLIENT_ID = Config.CLIENT_ID
CLIENT_SECRET = Config.CLIENT_SECRET
AUTHORIZATION_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
REDIRECT_URI = 'http://127.0.0.1:5000/home'
SCOPE = ['activity']


@app.route('/')
def login():
    url = f'{AUTHORIZATION_BASE_URL}?response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={" ".join(SCOPE)}'
    return render_template('login.html', url=url)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


