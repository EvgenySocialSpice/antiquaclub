from faker import Faker
from datetime import timedelta
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


def get_category_by_id(categories, category_name):
    for category in categories:
        if category["name"] == category_name:
            return category["id"]


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
                "password": generate_password_hash("1234"),
                "role_user": "user",   # аdmin/user
                "phone_confirmed": True,
                "email_confirmed": True
                }
        users.append(user)
    return users


def fake_items(item_list, categories, users):
    items = []
    for category in item_list:
        for item_name in item_list[category]:
            nom_price = random.randint(10, 600)
            step_price = random.randint(int(nom_price/10), int(nom_price/2))*100  # шаг от 10% до 50
            nom_price *= 100
            item = {"name": item_name,
                    "category_id": get_category_by_id(categories, category),
                    "year": random.randint(1560, 1950),
                    "description": choose_description(),
                    "reg_time": fake.date_time_between(start_date="-29d", end_date="-6d"),
                    "nom_price": nom_price,
                    "step_price": step_price,
                    "last_price": None,
                    "start_auction": fake.date_time_between(start_date='+10d', end_date="+14d").replace(second=0),
                    "success_end_time": None,
                    "step_time": random.randint(1, 20),  # minutes
                    "max_time_duration": random.randint(1, 24),  # hours
                    "seller_user_id": random.choice(users)["id"],
                    "buyer_user_id": None,
                    "status": "future_sale",
                    }
            items.append(item)
    return items


def tags_for_items(items, tags):
    tags_items = []
    for item in items:
        number_of_tags = random.randint(0, 4)  # количество тегов
        for _ in range(number_of_tags):
            tag_item = {"item_id": item["id"],
                        "tag_id": random.choice(tags)["id"]
                        }
            tags_items.append(tag_item)
    return tags_items


def load_data(data, model, get_id=True):
    db_session.bulk_insert_mappings(model, data, return_defaults=get_id)
    db_session.commit()
    return data


def fake_data_from_list(fake_list):
    things = []
    for thing_name in fake_list:
        thing = {"name": thing_name}
        things.append(thing)
    return things


def choose_random_item(items):
    item = random.choice(items)
    items.remove(item)
    return item, items


def get_random_user_id(users, seller_id):
    user = random.choice(users)
    while user["id"] == seller_id:
        user = random.choice(users)
    return user["id"]


def create_and_set_bet(item):
    item["start_auction"] = item["reg_time"] + timedelta(days=random.randint(1, 5))
    bet = {"user_id": item["seller_user_id"],
           "item_id": item["id"],
           "trans_time": item["start_auction"],
           "current_price": item["nom_price"],
           "bet_type": "start_sale"
           }

    return item, bet


def create_bets_for_items(users, item, bets):
    number_of_bets = random.randint(3, 25)
    current_price = item['nom_price']
    seller_id = item["seller_user_id"]
    bet = bets[-1].copy()
    bet["bet_type"] = "bet_sale"
    for _ in range(number_of_bets):
        rand_bet_time = random.randint(1, item['step_time']*60-1)
        buyer = get_random_user_id(users, seller_id)
        bet = bets[-1].copy()
        bet["trans_time"] += timedelta(seconds=rand_bet_time)
        bet["user_id"] = buyer
        bet["current_price"] = current_price
        current_price += item["step_price"]
        bets.append(bet)
    return bets


def fake_failed_sales(items, bets, items_to_change, failed_sales):
    for _ in range(failed_sales):
        item, items = choose_random_item(items)
        item, bet = create_and_set_bet(item)
        bets.append(bet)
        bet = bets[-1].copy()
        bet["bet_type"] = "failed_sale"
        bet["trans_time"] += timedelta(hours=item["max_time_duration"])
        bets.append(bet)
        item["status"] = "failed_sale"
        items_to_change.append(item)

    return items, bets, items_to_change


def fake_success_sales(items, bets, items_to_change, users, success_sales):
    for _ in range(success_sales):
        item, items = choose_random_item(items)
        item, bet = create_and_set_bet(item)
        bets.append(bet)
        bets = create_bets_for_items(users, item, bets)
        bet = bets[-1].copy()
        bet["trans_time"] += timedelta(minutes=item["step_time"])
        bet["bet_type"] = "success_sale"
        bets.append(bet)
        item["last_price"] = bet["current_price"]
        item["success_end_time"] = bet["trans_time"]
        item["buyer_user_id"] = bet["user_id"]
        item["status"] = "success_sale"
        items_to_change.append(item)

    return bets, items_to_change


def fake_bets(users, items, failed_sales=6, success_sales=18):
    bets = []
    items_to_change = []
    items, bets, items_to_change = fake_failed_sales(items, bets, items_to_change, failed_sales)
    bets, items_to_change = fake_success_sales(items, bets, items_to_change, users, success_sales)

    return bets, items_to_change


def update_items(items):
    db_session.bulk_update_mappings(Item, items)
    db_session.commit()


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

    tag_list = ["золото", "серебро", "бронза", "обсидиан", "фарфор", "дерево", "очень редкая вещь", "предмет из набора",
                "камень", "готика", "возрождение", "барокко", "клаcсицизм", "сталь", "эпическая", "средние века",
                "эпоха возрождения", "новое время"
                ]
    users = fake_users()
    users = load_data(users, User)

    categories = fake_data_from_list(items)
    categories = load_data(categories, Category)

    tags = fake_data_from_list(tag_list)
    tags = load_data(tags, Tag)

    items = fake_items(items, categories, users)
    items = load_data(items, Item)

    tags_items = tags_for_items(items, tags)
    load_data(tags_items, ItemTag, get_id=False)

    bets, items_to_change = fake_bets(users, items)
    load_data(bets, Bet, get_id=False)

    update_items(items_to_change)


if __name__ == "__main__":
    main()
