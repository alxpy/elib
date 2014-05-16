import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = 'sqlite:///sqlite.db'

engine = create_engine(DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import elib.models
    Base.metadata.create_all(bind=engine)