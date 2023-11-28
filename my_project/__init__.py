from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


app = Flask(__name__)
# For secret key
app.config['SECRET_KEY'] = 'a2852701f7354a86b0a291cabaaf9df3'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///luxefurnix.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


from my_project import route