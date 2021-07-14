from auctionapp.db import db_session
from auctionapp.models_db import Tag, Category, Item, User, Bet


# def get_items_by_category(category_name):
#     items = Item.query.filter(Category.name == category_name).all()
#     # user = User.query.filter(User.email == "kovalevamargarita@mail.ru").first()
#     item_list = []
#     # print(category)
#     if items:
#         for item in items:
#             item_list.append(f"{item.category} - {item.name} -{item.seller}")
#         return item_list
#     else:
#         return None
def get_items_by_category():
    categories = db_session.query(Category).all()
    list_categories = []
    if categories:
        for category in categories:
            list_categories.append(category.name)
            
    return list_categories


def get_items():
    user = db_session.query(Category).all()
    return user
