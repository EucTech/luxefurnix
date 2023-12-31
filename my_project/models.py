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
    profile_pic = db.Column(db.String(20), nullable=False, default='default_profile.jpg')
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.phone_number}')"


class Category(db.Model):
    """This is the product category data model"""
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    category_name = db.Column(db.String(100))
    products = db.relationship('Product', back_populates='category',  cascade='all, delete-orphan')

    def __repr__(self):
        return f"Category'({self.category_name})'"


class Product(db.Model):
    """This is a data Model for products"""
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    product_images = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='products')
    reviews = db.relationship('Review', back_populates='products')

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.product_desc}', '{self.price}', '{self.color}')"


class Review(db.Model):
    """This is a data model product reviews"""
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    fullname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    products = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', backref='author', lazy=True)

    def __repr__(self):
        return f"Review('{self.id}', '{self.fullname}', '{self.review_text}', '{self.rating}')"


class ShoppingCart(db.Model):
    """This is a data model for shopping cart"""
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total = db.Column(db.Float)


    def calculate_total(self):
        """Implement your logic to calculate the total based 
        on product price and quantity"""
        product = Product.query.get_or_404(self.product_id)
        self.total = product.price * self.quantity
    
    def __repr__(self):
        return f"ShoppingCart(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total})"