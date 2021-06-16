import auctionapp.config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


db_uri = auctionapp.config.DATABASE_URI
print(db_uri)
engine = create_engine(db_uri)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
