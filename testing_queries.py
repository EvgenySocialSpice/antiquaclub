from auctionapp.models_db import Category
from auctionapp.queiries import get_items_by_category, get_items


def print_list(rows):
    for row in rows:
        print(row)


if __name__ == "__main__":
    items_by_category = get_items_by_category()
    items = get_items()
    print_list(items_by_category)
