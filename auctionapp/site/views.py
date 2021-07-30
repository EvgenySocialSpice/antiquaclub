from flask import Blueprint, render_template
from auctionapp.site_func import get_categories_cache, get_ttl_hash
from auctionapp.queiries import get_items_limit

blueprint = Blueprint("site", __name__)


@blueprint.route('/')
def index():
    title = 'АнтиквА Аукцион онлайн'
    list_categories = get_categories_cache(ttl_hash=get_ttl_hash())
    items_list = get_items_limit(8)
    return render_template('site/index.html', page_title=title, categories=list_categories, items_list=items_list)


@blueprint.route('/about')
def about():
    title = 'О нас'
    categories = get_categories_cache()
    return render_template('site/about.html', page_title=title, categories=categories)


@blueprint.route('/contacts')
def contacts():
    title = 'Контакты'
    categories = get_categories_cache()
    return render_template('site/contacts.html', page_title=title, categories=categories)


@blueprint.route('/auction')
def auction():
    title = 'Открытые Лоты'
    categories = get_categories_cache()
    items_list = get_items_limit(12)
    return render_template('site/auction.html', page_title=title, categories=categories, items_list=items_list)


@blueprint.route('/popular')
def popular():
    title = 'Популярные Лоты'
    categories = get_categories_cache()
    items_list = get_items_limit(12)
    return render_template('site/popular.html', page_title=title, categories=categories, items_list=items_list)