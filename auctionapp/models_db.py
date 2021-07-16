from auctionapp.db import db

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    nickname = db.Column(db.String(), unique=True, nullable=False, index=True)
    email = db.Column(EmailType(), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(), unique=True, nullable=False)
    birth_date = db.Column(db.Date(), nullable=False)
    reg_datetime = db.Column(db.DateTime(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role_user = db.Column(db.String(15))
    item_sales = relationship("Item", lazy="joined", foreign_keys="Item.seller_user_id")
    item_purchases = relationship("Item", lazy="joined", foreign_keys="Item.buyer_user_id")
    bets = relationship("Bet", lazy="joined")
    phone_confirmed = db.Column(db.Boolean())
    email_confirmed = db.Column(db.Boolean())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.id}, {self.nickname}, {self.email}"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True, unique=True)
    items = relationship("Item", lazy="joined", foreign_keys="Item.category_id")

    def __repr__(self):
        return f"Category {self.id}, {self.name}"


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True)
    category_id = db.Column(db.Integer(), db.ForeignKey(Category.id), index=True, nullable=False)
    year = db.Column(db.String())
    description = db.Column(db.String())
    reg_time = db.Column(db.DateTime(), nullable=False)
    nom_price = db.Column(db.Integer(), nullable=False)
    step_price = db.Column(db.Integer())
    last_price = db.Column(db.Integer())
    start_auction = db.Column(db.DateTime())
    success_end_time = db.Column(db.DateTime())
    step_time = db.Column(db.Integer())  # максимамальное время ставки после первой в минутах
    max_time_duration = db.Column(db.Integer())
    seller_user_id = db.Column(db.Integer(), db.ForeignKey(User.id), index=True, nullable=False)
    buyer_user_id = db.Column(db.Integer(), db.ForeignKey(User.id), index=True)
    status = db.Column(db.String(), nullable=False, index=True)
    photo = db.Column(db.String(200))
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
    user_id = db.Column(db.Integer(), ForeignKey(User.id), index=True, nullable=False)
    item_id = db.Column(db.Integer(), ForeignKey(Item.id), index=True, nullable=False)
    trans_time = db.Column(db.DateTime(), nullable=False, index=True)
    current_price = db.Column(db.Integer(), index=True, nullable=False)
    bet_type = db.Column(db.String(20), index=True, nullable=False)
    user = relationship("User", lazy="joined", overlaps="bets")
    item = relationship("Item", lazy="joined", overlaps="bets")

    def __repr__(self):
        return f"bet {self.id} by {self.user_id} at {self.trans_time}"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, index=True, unique=True)
    items = relationship("ItemTag", lazy="joined")

    def __repr__(self):
        return f"Tag {self.id}: {self.name}"


class ItemTag(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer(), primary_key=True)
    item_id = db.Column(db.Integer(), ForeignKey(Item.id), index=True, nullable=False)
    tag_id = db.Column(db.Integer(), ForeignKey(Tag.id), index=True, nullable=False)
    item = relationship("Item", lazy="joined", overlaps="tags")
    tag = relationship("Tag", lazy="joined", overlaps="items")

    def __repr__(self):
        return f"Товар {self.item_id} тэг {self.tag_id}"


# def create_models():
#     Base.metadata.create_all(bind=engine)
