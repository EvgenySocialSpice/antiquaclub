from functools import lru_cache
from auctionapp.queiries import get_categories
from flask import abort
import time


@lru_cache()
def get_categories_cache(ttl_hash=None):
    del ttl_hash
    items = get_categories()
    if not items:
        abort(404)

    return items


def get_ttl_hash(seconds=300):
    return(time.time() / seconds)
