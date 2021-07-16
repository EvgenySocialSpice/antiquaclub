from flask import Flask, abort, flash, render_template, redirect, url_for
from auctionapp.models_db import Item

from flask import Flask, flash, render_template, redirect, url_for, abort
from auctionapp.db import db
from auctionapp.queiries import get_items_by_category, get_item_by_id, get_items_limit, get_categories
from auctionapp.site_func import get_categories_cache, get_ttl_hash


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'АнтиквА Аукцион онлайн'
        list_categories = get_categories_cache(ttl_hash=get_ttl_hash())
        items_list = get_items_limit(8)
        return render_template('site/index.html', page_title=title, categories=list_categories, items_list=items_list)


    @app.route('/about')
    def about():
        title = 'О нас'
        categories = get_categories_cache()
        return render_template('site/about.html', page_title=title, categories=categories)

    @app.route('/contacts')
    def contacts():
        title = 'Контакты'
        categories = get_categories_cache()
        return render_template('site/contacts.html', page_title=title, categories=categories)

    @app.route('/login')
    def login():
        title = 'Авторизация'
        categories = get_categories_cache()
        return render_template('user/login.html', page_title=title, categories=categories)

    @app.route('/auction')
    def auction():
        title = 'Открытые Лоты'
        categories = get_categories_cache()
        items_list = get_items_limit(12)
        return render_template('site/auction.html', page_title=title, categories=categories, items_list=items_list)

    @app.route('/popular')
    def popular():
        title = 'Популярные Лоты'
        categories = get_categories_cache()
        items_list = get_items_limit(12)
        return render_template('site/popular.html', page_title=title, categories=categories, items_list=items_list)

    @app.route('/category/<int:category_id>')
    def category(category_id):
        item_list = get_items_by_category(category_id)
        categories = get_categories_cache()
        if not item_list:
            abort(404)
        title = 'Лоты категории:'
        return render_template('site/category.html', page_title=title, item_list=item_list, categories=categories)

    @app.route('/product/<int:item_id>')
    def product(item_id):
        my_item = get_item_by_id(item_id)
        categories = get_categories_cache()
        if not item_id:
            abort(404)
        items_list = get_items_limit()
        return render_template('site/product.html', page_title=my_item.name, items_list=items_list,
                               item=my_item, categories=categories)

    return app
