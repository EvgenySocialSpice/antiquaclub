from faker import Faker
from datetime import datetime
import random
from auctionapp.db import db_session
from auctionapp.models_db import User, Tag, Item, ItemTag, Bet, Category, generate_password_hash
from transliterate import translit

fake = Faker('ru_Ru')


def choose_description():
    descriptions = ["Уникальная вещь из большой коллекции герцога",
                    "Изумительной красоты творение из коллекции известного коллекционера",
                    "Особенная вещь из редкой коллекции",
                    "Известная работа Франсуа Дебуа",
                    "Лот в идеальном состоянии",
                    "Редкий лот из коллекции короля",
                    "Лот в отличном состоянии, побывал во многих музеях мира",
                    "Состояние отличное, очень редкая вещь",
                    "Лот из вещей известного Н. Франкерштейна",
                    "Вещь из усыпальниц королей"
                    ]
    description = random.choice(descriptions)
    return description


def get_thing_by_id(things, thing_name):
    for thing in things:
        if thing["name"] == thing_name:
            return thing["id"]


def fake_users(num_rows=35):
    users = []
    for _ in range(num_rows):
        user_firstname = fake.first_name()
        user_lastname = fake.last_name()
        nickname = translit(user_firstname[:3]+user_lastname[:3]+str(random.randint(1, 99)), reversed=True)
        # генерация никнейма - 3 буквы имени + 3 буквы фамилии + рандомное число и перевод в транслит
        user = {"name": user_firstname,
                "last_name": user_lastname,
                "nickname": nickname.lower(),
                "email": fake.free_email(),
                "phone": fake.phone_number(),
                "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90),
                "reg_datetime": fake.date_time_between(start_date="-45d", end_date="-30d"),
                "password": "1234",
                "role_user": "user",   # аdmin/user
                "phone_confirmed": True,
                "email_confirmed": True
                }
        users.append(user)
    return users


def fake_items_not_complete(item_list, categories, users):
    items = []
    for category in item_list:
        for item_name in item_list[category]:
            nom_price = random.randint(10, 600)
            step_price = random.randint(int(nom_price/10), int(nom_price/2))*100  # шаг от 10% до 50
            nom_price *= 100
            item = {"name": item_name,
                    "category_id": get_thing_by_id(categories, category),
                    "year": random.randint(1560, 1950),
                    "description": choose_description(),
                    "reg_time": fake.date_time_between(start_date="-29d", end_date="-2d"),
                    "nom_price": nom_price,
                    "step_price": step_price,
                    "last_price": None,
                    "start_auction": fake.date_time_between(start_date='+10d', end_date="+14d").replace(second=0),
                    "success_end_time": None,
                    "step_time": random.randint(1, 20),  # minutes
                    "max_time_duration": random.randint(1, 24),  # hours
                    "seller_user_id": random.choice(users)["id"],
                    "buyer_user_id": None,
                    "status": "future_auction",
                    }
            items.append(item)
    return items


def tags_for_items(items, tags):
    number_of_tags = random.randint(0, 4)
    tags_items = []
    for item in items:
        item_id = get_thing_by_id(items, item)
        for _ in range(number_of_tags):
            tag_item = {"item_id": item_id,
                        "tag_id": random.choice(tags)['id']
                        }
            tags_items.append(tag_item)
    return tags_items


def load_items(items):
    db_session.bulk_insert_mappings(Item, items, return_defaults=True)
    db_session.commit()
    return items


def load_tags():
    tag_list = ["золото", "серебро", "бронза", "обсидиан", "фарфор", "дерево", "очень редкая вещь", "предмет из набора",
                "камень", "готика", "возрождение", "барокко", "клаcсицизм", "сталь", "эпическая", "средние века",
                "эпоха возрождения", "новое время"
                ]
    tags = []
    for tag_name in tag_list:
        tag = {"name": tag_name}
        tags.append(tag)
    db_session.bulk_insert_mappings(Tag, tags, return_defaults=True)
    db_session.commit()
    return tags


def load_categories(category_list):
    categories = []
    for category_name in category_list:
        category = {"name": category_name}
        categories.append(category)
    db_session.bulk_insert_mappings(Category, categories, return_defaults=True)
    db_session.commit()
    return categories


def load_users(users):
    db_session.bulk_insert_mappings(User, users, return_defaults=True)
    db_session.commit()
    return users


def main():
    items = {"Оружие": ["Кинжал офицера", "Рапира", "Меч Вильгельма", "Щит", "Шлем генерала", "Нагрудник",
                        "Меч Средних веков", "Сабля атамана"],
             "Ювелирные изделия": ["Кольцо ", "Колье герцога", "Кольцо из золота с бриллиантами", "Браслет принцессы",
                                   "Серьги Мари Пармоне", "Подвеска императрицы", "Цепь ганстера", "Брошь княгини"],
             "Картины": ["Буря в море", "Мона Мария", "Портрет офицера", "Шишкин лес", "Cеверная", "Горные приключения",
                         "Южные пейзажи", "Над вечным покоем"],
             "Мебель": ["Набор стульев", "Книжный шкаф", "Туалетный столик", "Кровать резная",
                        "Стол из красного дерева", "Подсвечник на  5 свечей", "Шкатулка для украшений",
                        "Письменный стол"],
             "Часы": ["Часы напольные", "Часы наручные", "Часы на цепочке", "Часы настенные", "Часы с фигурками",
                      "Часы инкрустированные камнями", "Часы резные", "Часы из камня"],
             "Марки": ["Коллекция 'СССР'", "Коллекция 'Современное искусство'", "Армия спасения", "Томас Иккерсон",
                       "Куба 'Железные дороги'", "Германия 'Машины'", "Италия 'Шахматы'", "Крайний север"]
             }
    users = fake_users()
    users = load_users(users)
    categories = load_categories(items)
    tags = load_tags()
    items = fake_items_not_complete(items, categories, users)
    items = load_items(items)
    tags_items = tags_for_items(items, tags)
    

if __name__ == "__main__":
    main()
