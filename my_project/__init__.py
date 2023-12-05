import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager


load_dotenv()
# MySQL database connection credentials
db_user = os.environ['DB_USER']
db_pwd = os.environ['DB_PWD']
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']

app = Flask(__name__)
# For secret key
app.config['SECRET_KEY'] = 'a2852701f7354a86b0a291cabaaf9df3'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{db_user}:{db_pwd}@{db_host}/{db_name}".format(
    db_user=db_user, db_pwd=db_pwd, db_host=db_host, db_name=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)



# when a user tries to access a protected resource without being
# logged in, they will be redirected to the login endpoint
login_manager.login_view = 'login'
# This allows you to style or handle these messages differently in your
# templates, such as showing them with a specific color or formatting.
login_manager.login_message_category = 'info'

from my_project import route