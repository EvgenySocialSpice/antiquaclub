from flask import Blueprint, render_template, abort
from auctionapp.site_func import get_categories_cache
from auctionapp.queiries import get_items_by_category, get_item_by_id, get_items_limit

blueprint = Blueprint("item", __name__)


@blueprint.route('/category/<int:category_id>')
def category(category_id):
    item_list = get_items_by_category(category_id)
    categories = get_categories_cache()
    if not item_list:
        abort(404)
    title = 'Лоты категории:'
    return render_template('item/category.html', page_title=title, item_list=item_list, categories=categories)


@blueprint.route('/product/<int:item_id>')
def product(item_id):
    my_item = get_item_by_id(item_id)
    categories = get_categories_cache()
    if not item_id:
        abort(404)
    items_list = get_items_limit()
    return render_template('item/product.html', page_title=my_item.name, items_list=items_list,
                           item=my_item, categories=categories)
