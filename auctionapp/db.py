# import auctionapp.config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://shsngduw:v-6Y3MWBdYHUtZJ_iz3Z73JH0kylhJOB@hattie.db.elephantsql.com/shsngduw')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# db_uri = auctionapp.config.DATABASE_URI
# engine = create_engine(db_uri)
# db_session = scoped_session(sessionmaker(bind=engine))
#
# Base = declarative_base()
# Base.query = db_session.query_property()
