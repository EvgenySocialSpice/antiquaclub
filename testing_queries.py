from auctionapp.models_db import Category
from auctionapp.queiries import get_categories, get_items_by_category


def print_list(rows):
    for row in rows:
        print(f"{row[0]} - id {row[1]} ")


def print_items(items):
    for item in items:
        print(f"{item.name} - {item.id}")


if __name__ == "__main__":
    categories = get_categories()

    print(categories)

    # items = get_items_by_category("Часы")
    # print_items(items)