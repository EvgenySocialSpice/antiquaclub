from auctionapp.db import db_session
from auctionapp.models_db import Tag, Category, Item, User, Bet


def get_items_by_category(category_name):
    category = Category.query.filter(Category.name == category_name).all()
    # user = User.query.filter(User.email == "kovalevamargarita@mail.ru").first()
    item_list = []
    
    if category:
        return category.items
        for item in category.items:
            item_list.append(f"{category.name} - {item.name} -{item.seller}")

    else:
        return None


def get_user_by_id():
    user = db_session.query(Item).all()
    return user
