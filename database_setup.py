""" SQLAlchemy Setup Module """
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

BASE = declarative_base()


class User(BASE):
    """ User Entity Class """
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    user_email = Column(String(250), nullable=False)
    user_picture = Column(String(250))
    user_provider = Column(String(80), nullable=False)

class Category(BASE):
    """ Category Entity Class """
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(200), nullable=False)
    category_description = Column(String(400))


class Item(BASE):
    """ Item Entity Class """
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(250), nullable=False)
    item_description = Column(String)
    item_picture = Column(String(250))
    item_price = Column(Float)
    item_register_date = Column(DateTime, default=datetime.datetime.now)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    Category = relationship(Category)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    User = relationship(User)

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'item_id': self.item_id,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'item_picture': self.item_picture,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'category_name': self.Category.category_name
        }

class Favourite(BASE):
    """ Favourite Entity Class """
    __tablename__ = "favourite"
    favourite_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    User = relationship(User)
    item_id = Column(Integer, ForeignKey("item.item_id"), nullable=False)
    Item = relationship(Item)
    favourite_date = Column(DateTime, default=datetime.datetime.now)

ENGINE = create_engine('sqlite:///catalog.db')
BASE.metadata.create_all(ENGINE)
