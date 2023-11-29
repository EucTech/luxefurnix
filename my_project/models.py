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
