from flask import Flask, flash, render_template, redirect, url_for, abort
from auctionapp.models_db import Base
from auctionapp.queiries import get_items_by_category, get_categories


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    # Base.init_app(app)
    
    @app.route('/')
    def index():
        title = 'АнтиквА Аукцион онлайн'
        list_categories = get_categories()
        if not list_categories:
            abort(404)
        return render_template('site/index.html', page_title=title, categories=list_categories)

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

    @app.route('/auction')
    def auction():
        title = 'Открытые Лоты'
        return render_template('site/auction.html', page_title=title)

    @app.route('/popular')
    def popular():
        title = 'Популярные Лоты'
        return render_template('site/popular.html', page_title=title)

    # @blueprint.route('/news/<int:news_id>')

    @app.route('/category/<int:category_id>')
    def category(category_id):
        item_list = get_items_by_category(category_id)
        
        if not item_list:
            abort(404)
        title = 'Лоты категории:'
        return render_template('site/category.html', page_title=title, item_list=item_list)

    @app.route('/product')
    def product():
        title = ''
        return render_template('site/product.html', page_title=title)

    return app
