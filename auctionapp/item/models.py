from auctionapp.db import db

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from auctionapp.user.models import User


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True, unique=True)
    items = relationship("Item", lazy="joined", foreign_keys="Item.category_id")

    def __repr__(self):
        return f"Category {self.id}, {self.name}"


class Item(db.Model):
    __tablename__ = "items"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True)
    category_id = Column(Integer(), ForeignKey(Category.id), index=True, nullable=False)
    year = Column(String())
    description = Column(String())
    reg_time = Column(DateTime(), nullable=False)
    nom_price = Column(Integer(), nullable=False)
    step_price = Column(Integer())
    last_price = Column(Integer())
    start_auction = Column(DateTime())
    success_end_time = Column(DateTime())
    step_time = Column(Integer())  # максимамальное время ставки после первой в минутах
    max_time_duration = Column(Integer())
    seller_user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    buyer_user_id = Column(Integer(), ForeignKey(User.id), index=True)
    status = Column(String(), nullable=False, index=True)
    photo = Column(String(200))
    category = relationship("Category", lazy="joined", overlaps="items")
    buyer = relationship("User", foreign_keys=[buyer_user_id], lazy="joined", overlaps="item_purchases")
    seller = relationship("User", foreign_keys=[seller_user_id], lazy="joined", overlaps="item_sales")
    bets = relationship("Bet", lazy="joined")
    tags = relationship("ItemTag", lazy="joined")

    def __repr__(self):
        return f"Item {self.id}, {self.name}"


class Bet(db.Model):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    item_id = Column(Integer(), ForeignKey(Item.id), index=True, nullable=False)
    trans_time = Column(DateTime(), nullable=False, index=True)
    current_price = Column(Integer(), index=True, nullable=False)
    bet_type = Column(String(20), index=True, nullable=False)
    user = relationship("User", lazy="joined", overlaps="bets")
    item = relationship("Item", lazy="joined", overlaps="bets")

    def __repr__(self):
        return f"bet {self.id} by {self.user_id} at {self.trans_time}"


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True, unique=True)
    items = relationship("ItemTag", lazy="joined")

    def __repr__(self):
        return f"Tag {self.id}: {self.name}"


class ItemTag(db.Model):
    __tablename__ = "items_tags"

    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey(Item.id), index=True, nullable=False)
    tag_id = Column(Integer(), ForeignKey(Tag.id), index=True, nullable=False)
    item = relationship("Item", lazy="joined", overlaps="tags")
    tag = relationship("Tag", lazy="joined", overlaps="items")

    def __repr__(self):
        return f"Товар {self.item_id} тэг {self.tag_id}"
