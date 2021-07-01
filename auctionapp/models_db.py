from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from auctionapp.db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    nickname = Column(String(), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(Integer(), unique=True, nullable=False)
    birth_date = Column(Date(), nullable=False)
    reg_datetime = Column(DateTime())
    password = Column(String())
    role_user = Column(String())
    items = relationship("Item", lazy="joined")

    def __repr__(self):
        return f"User {self.id}, {self.nickname}, {self.email}"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, index=True)
    items = relationship("Item", lazy="joined")

    def __repr__(self):
        return f"Category {self.id}, {self.name}"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False, index=True)
    category_id = Column(Integer(), ForeignKey(Category.id), index=True, nullable=False)
    # tags = Column(ARRAY(String(10)))
    year = Column(String())
    description = Column(String())
    reg_time = Column(DateTime())
    nom_price = Column(Integer())
    step_price = Column(Integer())
    last_price = Column(Integer())
    start_auction = Column(DateTime())
    max_time_duration = Column(Time())
    seller_user_id = Column(Integer(), ForeignKey(User.id), index=True, nullable=False)
    buyer_user_id = Column(Integer(), ForeignKey(User.id), index=True)
    status = Column(String(), nullable=False, index=True)
    category = relationship("Category", lazy="joined")
    users = relationship("User", lazy="joined")
    bets = relationship("Bet", lazy="joined")

    def __repr__(self):
        return f"Item {self.id}, {self.name}"


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer(), ForeignKey(User.id), index=True)
    item_id = Column(Integer(), ForeignKey(Item.id), index=True)
    trans_time = Column(DateTime())
    current_price = Column(Integer())
    user = relationship("User", lazy="joined")
    item = relationship("Item", lazy="joined")

    def __repr__(self):
        return f"bet {self.id} by {self.user_id} at {self.trans_time}"


# class Tag(Base):
#     __tablename__ = "tags"

#     id = Column(Integer(), primary_key=True)
#     name = Column(String(50))
#     tags_items_ids = Column(ARRAY(ForeignKey(Items.id)))

#     def __repr__(self):
#         return f"Item {self.id}, {self.name}"


def create_models():
    Base.metadata.create_all(bind=engine)

