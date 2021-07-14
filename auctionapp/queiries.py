from auctionapp.db import db_session
from auctionapp.models_db import Tag, Category, Item, User, Bet


def get_categories():
    categories = db_session.query(Category.name).all()
    list_categories = []
    if categories:
        for category in categories:
            list_categories.append(category.name)

    return list_categories


def get_items_by_category(category_name):
    items = db_session.query(Item).join(Category, Item.category_id == Category.id).filter(
            Category.name == category_name).all()

    return items
