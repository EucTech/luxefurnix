from my_project import db
from datetime import datetime
import uuid
"""This is a file for database"""


class User(db.Model):
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
