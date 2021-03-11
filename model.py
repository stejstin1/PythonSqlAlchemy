import os

from sqlalchemy import Column, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)#auto incremets since it is a primary key
    username = Column(String(80))
    password = Column(String(80))


db_name = 'data.db'
if os.path.exists(db_name):
    os.remove(db_name)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///' + db_name)

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)