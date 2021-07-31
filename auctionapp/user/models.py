from auctionapp.db import db
from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    nickname = Column(String(), unique=True, nullable=False, index=True)
    email = Column(EmailType(), unique=True, nullable=False, index=True)
    phone = Column(String(), unique=True, nullable=False)
    birth_date = Column(Date(), nullable=False)
    reg_datetime = Column(DateTime(), nullable=False)
    password = Column(String(), nullable=False)
    role_user = Column(String(15))
    item_sales = relationship("Item", lazy="joined", foreign_keys="Item.seller_user_id")
    item_purchases = relationship("Item", lazy="joined", foreign_keys="Item.buyer_user_id")
    bets = relationship("Bet", lazy="joined")
    phone_confirmed = Column(Boolean())
    email_confirmed = Column(Boolean())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.id}, {self.nickname}, {self.email}"
