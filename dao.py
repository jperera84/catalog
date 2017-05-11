""" Data Access Module """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import BASE, User, Category, Item, Favourite

# Connect to Database and create database session
ENGINE = create_engine('sqlite:///catalog.db')
BASE.metadata.bind = ENGINE

DBSESSION = sessionmaker(bind=ENGINE)
SESSION = DBSESSION()

def get_all_categories():
    """ Get All Categories """
    categories = SESSION.query(Category).all()
    return categories

def get_category_by_id(category_id):
    """ Get Category By ID """
    category = SESSION.query(Category).filter_by(category_id=category_id).first()
    return category

def insert_category(category):
    """ Insert Category """
    SESSION.add(category)
    SESSION.commit()
    return category.category_id

def update_category(category_id, category):
    """ Update Category """
    category_bd = SESSION.query(Category).filter_by(category_id=category_id).first()
    category_bd.category_name = category.category_name
    category_bd.category_description = category.category_description
    SESSION.add(category_bd)
    SESSION.commit()

def delete_category(category_id):
    """ Delete Category """
    category = SESSION.query(Category).filter_by(category_id=category_id).first()
    if category:
        SESSION.delete(category)
        SESSION.commit()

def get_all_users():
    """ Get All Users """
    users = SESSION.query(User).all()
    return users

def get_user_by_id(user_id):
    """ Get Users by email """
    user = SESSION.query(User).filter_by(user_id=user_id).first()
    return user

def get_user_by_email(email):
    """ Get Users by email """
    users = SESSION.query(User).filter_by(user_email=email).all()
    return users

def get_user_by_email_provider(email, provider):
    """ Get Users by email and provider """
    user = SESSION.query(User).filter_by(user_email=email, user_provider=provider).first()
    return user

def insert_user(user):
    """ Insert User """
    SESSION.add(user)
    SESSION.commit()
    return user.user_id

def update_user(email, provider, user):
    """ Update User Info """
    user_bd = SESSION.query(User).filter_by(user_email=email, user_provider=provider).first()
    if user_bd:
        user_bd.user_name = user.user_name
        user_bd.user_picture = user.user_picture
        SESSION.add(user_bd)
        SESSION.commit()

def delete_user(user_id):
    """ Delete User """
    user = SESSION.query(User).filter_by(user_id=user_id).first()
    if user:
        SESSION.delete(user)
        SESSION.commit()

def get_lates_items():
    """ Return the 10 latest items added """
    items = SESSION.query(Item).order_by(Item.item_register_date.desc()).limit(10)
    return items

def get_item_by_id(item_id):
    """ Get Item by id """
    item = SESSION.query(Item).filter_by(item_id=item_id).first()
    return item

def get_items_by_category(category_id):
    """ Return Items by Category """
    items = SESSION.query(Item).filter_by(category_id=category_id).order_by(Item.item_register_date.desc()).all()
    return items

def get_item_favourite(item_id, user_id):
    """ Return Items Favourite """
    item = SESSION.query(Item).filter_by(item_id=item_id, user_id=user_id).first()
    return item

def get_all_items():
    """ Return Items by Category """
    items = SESSION.query(Item).order_by(Item.item_register_date.desc()).all()
    return items

def insert_item(item):
    """ Insert New Item """
    SESSION.add(item)
    SESSION.commit()
    return item.item_id

def update_item(item_id, item):
    """ Update the Item """
    item_bd = SESSION.query(Item).filter_by(item_id=item_id).first()
    if item_bd:
        item_bd.item_name = item.item_name
        item_bd.item_description = item.item_description
        item_bd.item_picture = item.item_picture
        item_bd.item_price = item.item_price
        SESSION.add(item_bd)
        SESSION.commit()

def delete_item(item_id):
    """ Delete Item """
    item_bd = SESSION.query(Item).filter_by(item_id=item_id).first()
    if item_bd:
        SESSION.delete(item_bd)
        SESSION.commit()

def insert_favourite(item_id, user_id):
    """ Insert New Favourite Item For User """
    fav = Favourite(user_id=user_id, item_id=item_id)
    SESSION.add(fav)
    SESSION.commit()
    return fav.favourite_id

def delete_favourite(item_id, user_id):
    """ Delete Favourite """
    fav_bd = SESSION.query(Favourite).filter_by(item_id=item_id, user_id=user_id).first()
    if fav_bd:
        SESSION.delete(fav_bd)
        SESSION.commit()
