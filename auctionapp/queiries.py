from auctionapp.db import db_session
from auctionapp.models_db import Tag, Category, Item, User, Bet


def get_categories():
    categories = db_session.query(Category.name, Category.id).all()
    list_categories = []
    if categories:
        for category in categories:
            list_categories.append({"name": category.name, "id": category.id})
    db_session.close()
    return list_categories


def get_items_by_category(category_id):
    items = db_session.query(Item).join(Category, Item.category_id == Category.id).filter(
            Category.id == category_id).all()

    db_session.close()

    return items


def get_item_by_id(item_id):
    item = Item.query.filter(Item.id == item_id).first()

    db_session.close()

    return item
    

def get_items_limit(number=4):
    items_list = Item.query.limit(number).all()
    db_session.close()

    return items_list

