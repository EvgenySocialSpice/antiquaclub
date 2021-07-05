from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Boolean
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from auctionapp.db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    nickname = Column(String(), unique=True, nullable=False, index=True)
    email = Column(EmailType(), unique=True, nullable=False, index=True)
    phone = Column(Integer(), unique=True, nullable=False)
    birth_date = Column(Date(), nullable=False)
    reg_datetime = Column(DateTime(), nullable=False)
    password = Column(String(), nullable=False)
    role_user = Column(String(15))
    items = relationship("Item", lazy="joined")
    bets = relationship("Bet", lazy="joined")
    phone_confirmed = Column(Boolean())
    email_confirmed = Column(Boolean())

    def __repr__(self):
        return f"User {self.id}, {self.nickname}, {self.email}"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True, unique=True)
    items = relationship("Item", lazy="joined")

    def __repr__(self):
        return f"Category {self.id}, {self.name}"


class Item(Base):
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
    max_time_duration = Column(Time())
    seller_user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    buyer_user_id = Column(Integer(), ForeignKey(User.id), index=True)
    status = Column(String(), nullable=False, index=True)
    category = relationship("Category", lazy="joined")
    users = relationship("User", lazy="joined")
    bets = relationship("Bet", lazy="joined")
    tags = relationship("ItemTag", lazy="joined")

    def __repr__(self):
        return f"Item {self.id}, {self.name}"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    item_id = Column(Integer(), ForeignKey(Item.id), index=True, nullable=False)
    trans_time = Column(DateTime(), nullable=False, index=True)
    current_price = Column(Integer(), index=True, nullable=False)
    bet_type = Column(String(20), index=True, nullable=False)
    user = relationship("User", lazy="joined")
    item = relationship("Item", lazy="joined")

    def __repr__(self):
        return f"bet {self.id} by {self.user_id} at {self.trans_time}"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True, unique=True)
    items = relationship("ItemTag", lazy="joined")

    def __repr__(self):
        return f"Tag {self.id}, {self.name}"


class ItemTag(Base):
    __tablename__ = "items_tags"

    id = Column(Integer(), primary_key=True)
    item_id = Column(Integer(), ForeignKey(Item.id), index=True, nullable=False)
    tag_id = Column(Integer(), ForeignKey(Tag.id), index=True, nullable=False)
    item = relationship("ItemTag", lazy="joined")
    tag = relationship("Tag", lazy="joined")

    def __repr__(self):
        return f"Товар {self.item_id} тэг {self.tag_id}"


def create_models():
    Base.metadata.create_all(bind=engine)