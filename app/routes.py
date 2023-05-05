from . import app
from flask import render_template, redirect, url_for


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


