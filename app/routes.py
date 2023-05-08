from . import app
from flask import render_template, redirect, url_for
from config import Config
from flask import render_template, redirect, url_for
from .form import LoginForm, RegisterForm

CLIENT_ID = Config.CLIENT_ID
CLIENT_SECRET = Config.CLIENT_SECRET
AUTHORIZATION_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
REDIRECT_URI = 'http://127.0.0.1:5000/home'
SCOPE = ['activity']


@app.route('/')
def main():
    #url = f'{AUTHORIZATION_BASE_URL}?response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={" ".join(SCOPE)}'
    url1 = '/login'
    url2 = '/register'
    return render_template('main.html', url1=url1, url2=url2)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

