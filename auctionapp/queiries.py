from auctionapp.db import db
from auctionapp.user.models import User
from auctionapp.item.models import Tag, Category, Item, Bet


def get_categories():
    categories = db.session.query(Category.name, Category.id).all()
    list_categories = []
    if categories:
        for category in categories:
            list_categories.append({"name": category.name, "id": category.id})
    return list_categories


def get_items_by_category(category_id):
    # items = db.session.query(Item).filter(
    #         Item.category_id == category_id).all()
    list_items = []
    items = db.session.query(Item.name, Item.id, Item.description, Item.status, Item.photo, Item.last_price,
                             Item.nom_price, Item.year).filter(Item.category_id == category_id).all()
    if items:
        for item in items:
            list_items.append({"id": item.id, "name": item.name, "description": item.description, "status": item.status,
                               "photo": item.photo, "last_price": item.last_price, "year": item.year})
    return items


def get_item_by_id(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    return item


def get_items_limit(number=4):
    items_list = Item.query.limit(number).all()
    return items_list
