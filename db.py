import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, Boolean

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///' + os.getcwd() + '/data/store.db', echo=True)


class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True)
    bid = Columng(String, unique=True)

    price_range = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    credit_card = Column(Boolean)

    def __repr__(self):
        return '<Business bid=%s>' % (self.bid, )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)

    review_count = Column(Integer)
    num_fans = Column(Integer)
    years_elite = Column(Integer)

    funny = Column(Integer)
    useful = Column(Integer)
    cool = Column(Integer)

    def __repr__(self):
        return '<User uid=%s>' % (self.uid, )


class Tip(Base):
    __tablename__ = 'tips'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    bid = Column(String)
    likes = Column(Integer)

    def __repr__(self):
        return '<Tip bid=%s uid=%s>' % (self.bid, self.uid)
