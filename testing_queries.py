from auctionapp.queiries import get_items_by_category, get_user_by_id

if __name__ == "__main__":
    items_by_category = get_items_by_category("Часы")
    # items = get_user_by_id()
    for item in items_by_category:
        print(f"{item.name} -{item.reg_time}" )