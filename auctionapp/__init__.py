from flask import Flask, flash, render_template, redirect, url_for
from auctionapp.models_db import Base


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    Base.init_app(app)

    @app.route('/')
    def index():
        title = 'АнтиквА Аукцион онлайн'
        return render_template('site/index.html', page_title=title)

    @app.route('/about')
    def about():
        title = 'О нас'
        return render_template('site/about.html', page_title=title)

    @app.route('/contacts')
    def contacts():
        title = 'Контакты'
        return render_template('site/contacts.html', page_title=title)

    @app.route('/login')
    def login():
        title = 'Авторизация'
        return render_template('user/login.html', page_title=title)

    return app
