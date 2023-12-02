import os
from my_project import db, login_manager
from datetime import datetime
import uuid
from flask_login import UserMixin
"""
    This is a file for database

    The UserMixin class provides default implementations 
    for methods is_authenticated, is_active, is_anonymous, 
    and get_id to work seamlessly with Flask-Login
"""


@login_manager.user_loader
def load_user(user_id):
    """This function is a flask_login method that
        loads the Users ID from the database
    """
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """Class for User data"""
    # The lambda function on the id ensure that a new id is created at every instance
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    fullname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='profile_default_pic.jpg')
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.phone_number}')"


# class Category(db.Model):
#     """This is the product category data model"""
#     id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
#     category_name = db.Column(db.String(100))
#     products = db.relationship('Product', back_populates='category')

#     def __repr__(self):
#         return f"Category'({self.category_name})'"


class Product(db.Model):
    """This is a data Model for products"""
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    product_images = db.Column(db.String(20), nullable=False, default='default-product.png')
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category', back_populates='products')

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_desc}', '{self.price}', '{self.color}')"

