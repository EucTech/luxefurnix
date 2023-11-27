from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# For secret key
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///luxefurnix.db"

db = SQLAlchemy(app)


from my_project import route