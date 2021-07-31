from flask import Blueprint, render_template
from auctionapp.site_func import get_categories_cache

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route('/login')
def login():
    title = 'Авторизация'
    categories = get_categories_cache()
    return render_template('user/login.html', page_title=title, categories=categories)


