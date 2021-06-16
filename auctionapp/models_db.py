from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, Date, ARRAY, Time, engine

from auctionapp.db import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String())
    email = Column(String(120), unique=True)
    phone = Column(Integer(), unique=True)
    birth_date = Column(Date())
    reg_datetime = Column(DateTime())

    def __repr__(self):
        return f"User {self.id}, {self.name}, {self.email}"


class Items(Base):
    __tablename__ = "items_auction"

    id = Column(Integer, primary_key=True)
    name = Column(String())
    category = Column(String())
    tags = Column(ARRAY(String(10)))
    price = Column(Integer())
    step_price = Column(Integer())
    start_auction = Column(DateTime())
    max_time_auction = Column(Time())
    buyer = Column(Integer)

    def __repr__(self):
            return f"Item {self.id}, {self.name}"


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
