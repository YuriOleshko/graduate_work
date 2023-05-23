from . import app
from .models import User, db
from config import Config
from flask import render_template, redirect, url_for, request, session
from .form import LoginForm, RegisterForm, FeedbackForm
from flask_login import LoginManager, login_user, current_user
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient




CLIENT_ID = Config.CLIENT_ID
CLIENT_SECRET = Config.CLIENT_SECRET
AUTHORIZATION_BASE_URL = 'https://www.fitbit.com/oauth2/authorize'
REDIRECT_URI = 'http://127.0.0.1:5000/home'
TOKEN_URL = 'https://api.fitbit.com/oauth2/token'
SCOPE = ['profile']
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
def main():
    url1 = '/login'
    url2 = '/register'
    return render_template('main.html', url1=url1, url2=url2)


@app.route('/home')
def home():
    if current_user.is_authenticated:
        client = BackendApplicationClient(client_id=CLIENT_ID)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=TOKEN_URL, client_id=CLIENT_ID,
                                      client_secret=CLIENT_SECRET, scope=SCOPE)
        session['fitbit_token'] = token['access_token']  # Сохраняем токен в сессии

        # Получаем токен из сессии при каждом запросе
        access_token = session['fitbit_token']

        # Создаем объект OAuth2Session с переданным токеном
        oauth = OAuth2Session(client_id=CLIENT_ID, token={'access_token': access_token}, scope=SCOPE)

        # Делаем запрос к API Fitbit, передавая токен в заголовке
        response = oauth.get("https://api.fitbit.com/1/user/-/profile.json")
        return response.json()
        #return redirect(url_for('user_home', user_id=current_user.id))
    else:
        return redirect(url_for('login'))



@app.route('/home/user/<int:user_id>')
def user_home(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('user_home.html', user=user)
    else:
        return redirect(url_for('register'))



@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/feedback')
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        # обрабатываем отправку формы
        return 'Thank you for your review!'
    return render_template('feedback.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')

        # Проверка аутентификации пользователя
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user, remember=remember)
            return redirect(url_for('home'))
        else:
            text = 'Username or password is not correct'
            return render_template('login.html', form=form, text=text)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            text = 'Username already exists'
            return render_template('register.html', form=form, text=text)

        user = User.query.filter_by(email=email).first()
        if user:
            text1 = 'Email already exists'
            return render_template('register.html', form=form, text1=text1)


        user = User(username=username, email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'An error occurred during registration'
    else:
        return render_template('register.html', form=form)

